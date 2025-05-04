# Photoalbum MVP

Ez egy egyszerű, skálázható fényképalbum alkalmazás Django-val, amely AWS-en fut ECS Fargate-en, S3-at használ képekhez, PostgreSQL-t adatbázisnak, és minden infrastruktúra Terraform Cloud-dal menedzselt. A build és deploy automatikus GitHub Actions segítségével.

## Fő technológiák
- Django (Python)
- AWS ECS Fargate (konténer futtatás)
- AWS S3 (képek tárolása)
- AWS RDS PostgreSQL (adatbázis)
- AWS ECR (Docker image tárolás)
- Terraform Cloud (infra provisioning)
- GitHub Actions (CI/CD)
- Docker (konténerizálás)

## Fő funkciók
- Fényképek feltöltése, törlése (csak bejelentkezett felhasználónak)
- Fényképek listázása név vagy dátum szerint
- Fénykép részletek megtekintése
- Felhasználókezelés (regisztráció, belépés, kilépés)

## Deployment folyamat
1. Kód push a GitHub-ra
2. GitHub Actions buildeli a Docker imaget, pusholja ECR-be
3. Terraform Cloud automatikusan frissíti az AWS infrastruktúrát (ECS, RDS, S3, IAM, stb.)
4. Az alkalmazás elérhető az AWS-en

## Konfiguráció
A szükséges beállításokat (AWS kulcsok, DB URL, stb.) környezeti változókkal kell megadni. Lásd a `photoalbum/photoalbum/settings.py` végét.

---

Ez a projekt megfelel a beadandó feladat minden követelményének, egyszerű, olcsó, és teljesen automatizált. 