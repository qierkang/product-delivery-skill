#!/usr/bin/env bash
set -euo pipefail

WEB_URL="${WEB_URL:-http://127.0.0.1:18080}"
API_URL="${API_URL:-http://127.0.0.1:18081}"
MANAGE_URL="${MANAGE_URL:-http://127.0.0.1:18082}"

echo "[smoke] health check"
curl -fsS "${API_URL}/health" >/dev/null
curl -fsS -o /dev/null "${WEB_URL}"
curl -fsS -o /dev/null "${MANAGE_URL}"

echo "[smoke] api check"
API_URL="${API_URL}" node <<'NODE'
const base = process.env.API_URL;

async function post(url, body, headers = {}) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...headers },
    body: JSON.stringify(body),
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(`${url} -> ${response.status} ${payload.message || ''}`);
  }
  return payload;
}

async function getJson(url, headers = {}) {
  const response = await fetch(url, { headers });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(`${url} -> ${response.status} ${payload.message || ''}`);
  }
  return payload;
}

(async () => {
  const sessionId = `smoke_${Date.now()}`;
  const bootstrap = await post(`${base}/api/session/bootstrap`, { sessionId, landingUrl: '/', channelCode: 'smoke-script' });
  const questions = await getJson(`${base}/api/tests/questions`);
  const answers = questions.questions.map((q, index) => ({ questionKey: q.key, value: q.key === 'q31' ? 2 : (index % 3) + 1 }));
  const submit = await post(`${base}/api/tests/submit`, {
    sessionId,
    nickname: bootstrap.nickname,
    durationSeconds: 66,
    answers,
  });
  await getJson(`${base}/api/reports/${submit.reportToken}`);
  await post(`${base}/api/reports/${submit.reportToken}/poster`, {});
  const login = await post(`${base}/api/manage/login`, { username: 'admin', password: 'sbti-red123' });
  await getJson(`${base}/api/manage/dashboard`, { 'x-admin-token': login.token });
  console.log(JSON.stringify({ ok: true, sessionId, reportToken: submit.reportToken }, null, 2));
})().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
NODE

echo "[smoke] done"
