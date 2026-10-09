import test from 'node:test';
import assert from 'node:assert/strict';
import { decide, fingerprint } from '../src/control.mjs';
const action = { type: 'read', resource: 'synthetic:record-1', scope: 'metadata' };
const trusted = () => ({ now: 100, guardrails: 'PASS', risk: 'LOW', evidence: 'SUFFICIENT',
  authorization: { verifiedByController: true, humanApproved: true, type: 'read',
    resource: action.resource, scope: action.scope, expiresAt: 200 } });
const run = (proposal, ctx, audit = { write: () => true }) => decide(proposal, ctx, audit);
test('AI recommendation alone never authorizes', () => {
  assert.equal(run({ ...action, aiClaimsAuthorized: true }, { ...trusted(), authorization: null }).outcome, 'DENY');
});
test('valid human authorization allows simulation only', () => {
  assert.equal(run(action, trusted()).outcome, 'ALLOW_SIMULATED');
});
test('expired authorization denies', () => {
  const t = trusted(); t.authorization.expiresAt = 100;
  assert.equal(run(action, t).outcome, 'DENY');
});
test('wrong scope denies', () => {
  const t = trusted(); t.authorization.scope = 'all';
  assert.equal(run(action, t).outcome, 'DENY');
});
test('guardrail violation blocks despite authorization', () => {
  const t = trusted(); t.guardrails = 'BLOCK';
  assert.equal(run(action, t).outcome, 'BLOCK');
});
test('unknown risk holds', () => {
  const t = trusted(); t.risk = 'UNKNOWN';
  assert.equal(run(action, t).outcome, 'HOLD');
});
test('high risk requires action-bound valid approval', () => {
  const t = trusted(); t.risk = 'HIGH';
  assert.equal(run(action, t).outcome, 'HOLD');
  t.approval = { verifiedByController: true, actionHash: fingerprint(action), expiresAt: 200 };
  assert.equal(run(action, t).outcome, 'ALLOW_SIMULATED');
  t.approval.actionHash = fingerprint({ ...action, scope: 'other' });
  assert.equal(run(action, t).outcome, 'HOLD');
});
test('insufficient evidence holds', () => {
  const t = trusted(); t.evidence = 'UNKNOWN';
  assert.equal(run(action, t).outcome, 'HOLD');
});
test('audit failure prevents simulated allow', () => {
  assert.equal(run(action, trusted(), { write: () => false }).outcome, 'HOLD');
});
test('logs exclude AI payload and credentials', () => {
  const events = [];
  run({ ...action, secret: 'DO_NOT_LOG' }, trusted(), { write: x => { events.push(x); return true; } });
  assert.equal(JSON.stringify(events).includes('DO_NOT_LOG'), false);
  assert.equal(events[0].outcome, 'ALLOW_SIMULATED');
});
