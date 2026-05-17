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
| Que herramienta de secret scanning debe usarse en CI/CD? | Security/DevOps | Phase 2 | Open | Candidate tools include Gitleaks or equivalent. |
| Debe existir un proceso para deshabilitar seed admin fuera de development? | Security/Ops | Before staging | Open | Fase 1 blocks weak seed password but does not remove seed flow. |
| Existing databases creadas con `create_all` deben ser stamped o recreadas localmente? | Engineering/DevOps | Before shared DB migration | Open | Decide per environment after schema comparison. |
| Que indices se necesitan para consultas frecuentes de `delivery_events` y `audit_logs`? | Engineering/Ops | Before performance hardening | Open | Baseline preserves current model; query-driven indexes come later. |
| Cuando se formalizara una tabla `orders`? | Product/Engineering | Future data model phase | Open | Current system uses `order_number` string. |
| Que warning cleanup se prioriza primero: Pydantic Config o timestamps UTC? | Engineering | Fase 4 or maintenance sprint | Open | Fase 3 leaves backend tests passing but noisy. |
| En que fase se agrega CI/CD para ejecutar backend/frontend tests? | DevOps/Engineering | Before production hardening | Open | Fase 3 documents commands but does not automate them. |
| Debe auditarse `OCR_CONFIRMED` como accion critica separada? | Security/Product | Before audit hardening | Open | Fase 3 covers implemented audit actions and documents this gap. |
| Se requiere prueba E2E browser para dashboard/mapa antes de demo? | Product/Engineering | Before client/demo readiness | Open | Frontend tests mock Leaflet and API. |
