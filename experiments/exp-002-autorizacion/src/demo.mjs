import { decide } from './control.mjs';
const proposal = { type: 'read', resource: 'synthetic:record-1', scope: 'metadata' };
const audit = { write: event => { console.log(JSON.stringify(event)); return true; } };
const trusted = { now: 100, guardrails: 'PASS', risk: 'LOW', evidence: 'SUFFICIENT',
  authorization: { verifiedByController: true, humanApproved: true, type: 'read',
    resource: 'synthetic:record-1', scope: 'metadata', expiresAt: 200 } };
console.log(decide(proposal, trusted, audit));
