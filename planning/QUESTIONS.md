# Questions

| Question | Owner | Needed By | Status | Answer / Notes |
| --- | --- | --- | --- | --- |
| Cuales son los estados oficiales de una orden? | Product/Ops | Phase 1 planning | Open | Required to normalize status reporting and validation. |
| Que evidencia es obligatoria por tipo de entrega? | Product/Ops | Before workflow hardening | Open | Required for upload requirements and supervisor review rules. |
| Que SLA debe tener la revision humana? | Product/Ops | Before metrics dashboard | Open | Required for `human_review_sla_minutes`. |
| Quien puede ver evidencia fotografica? | Security/Product | Before production | Open | Required because `/uploads` may expose sensitive evidence. |
| Como se asignan ordenes a drivers? | Product/Ops | Before driver workflow hardening | Open | Required because current `USER` to `Driver` relationship is not strong. |
| Que pasa si OCR falla? | Product/Ops | Before OCR production use | Open | Decide retry, manual fallback, and audit behavior. |
| Que pasa si OCR tiene baja confianza? | Product/Ops | Before OCR production use | Open | Decide threshold, review priority, and required manual fields. |
| Que metricas debe ver un supervisor? | Product/Ops | Before dashboard expansion | Open | Candidate metrics are pending reviews, review SLA, upload success, rejected OCR. |
| Que metricas debe ver direccion? | Leadership/Product | Before executive reporting | Open | Candidate metrics are order coverage, review throughput, operational exceptions. |
| Cuando se debe archivar o eliminar evidencia? | Security/Ops | Before production | Open | Required for retention and deprovisioning policy. |
| Que ambiente sera primero: dev, staging o produccion? | Engineering/DevOps | Phase 1 | Open | Required for secrets, CORS, deployment, and CI/CD design. |
| Se debe mantener `/uploads` publico en local solamente? | Security/Engineering | Phase 1 | Open | Current architecture serves uploads statically through FastAPI. |
| Que acciones adicionales deben auditarse? | Security/Product | Phase 1 | Open | Current audit coverage is minimal but useful. |
