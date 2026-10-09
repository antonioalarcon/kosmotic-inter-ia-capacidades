import { createHash } from 'node:crypto';

const fingerprint = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');
const fail = (outcome, reason, action, audit) => {
  const event = { action_ref: fingerprint(action), outcome, reason, policy_version: '0.1.0' };
  try { if (audit.write(event) !== true) return { outcome: 'HOLD', reason: 'AUDIT_UNAVAILABLE' }; }
  catch { return { outcome: 'HOLD', reason: 'AUDIT_UNAVAILABLE' }; }
  return { outcome, reason };
};

// All authorization data comes from the trusted controller, NEVER from an AI proposal.
// This is a synthetic, in-process demonstration, not identity verification or production authorization.
export function decide(proposal, trusted, audit) {
  if (!proposal || typeof proposal !== 'object' || !trusted || typeof trusted !== 'object' || !audit || typeof audit.write !== 'function')
    return { outcome: 'HOLD', reason: 'INVALID_INPUT_OR_AUDIT' };
  const action = { type: proposal.type, resource: proposal.resource, scope: proposal.scope };
  if ([action.type, action.resource, action.scope].some(x => typeof x !== 'string' || !x.trim()))
    return fail('DENY', 'INVALID_ACTION', action, audit);
  if (trusted.guardrails !== 'PASS') return fail('BLOCK', 'GUARDRAILS_NOT_VERIFIED', action, audit);
  const a = trusted.authorization;
  if (!a || a.verifiedByController !== true || a.humanApproved !== true)
    return fail('DENY', 'NO_VERIFIED_HUMAN_AUTHORIZATION', action, audit);
  if (a.type !== action.type || a.resource !== action.resource || a.scope !== action.scope)
    return fail('DENY', 'SCOPE_MISMATCH', action, audit);
  if (!Number.isFinite(trusted.now) || !Number.isFinite(a.expiresAt) || a.expiresAt <= trusted.now)
    return fail('DENY', 'AUTHORIZATION_EXPIRED_OR_UNKNOWN', action, audit);
  if (!['LOW', 'MEDIUM', 'HIGH'].includes(trusted.risk))
    return fail('HOLD', 'RISK_UNKNOWN', action, audit);
  if (trusted.risk === 'HIGH' && !(trusted.approval?.verifiedByController === true &&
      trusted.approval?.actionHash === fingerprint(action) &&
      Number.isFinite(trusted.approval.expiresAt) && trusted.approval.expiresAt > trusted.now))
    return fail('HOLD', 'SPECIFIC_APPROVAL_REQUIRED', action, audit);
  if (trusted.evidence !== 'SUFFICIENT') return fail('HOLD', 'EVIDENCE_INSUFFICIENT', action, audit);
  return fail('ALLOW_SIMULATED', 'ALL_CONTROLS_PASSED', action, audit);
}
export { fingerprint };
