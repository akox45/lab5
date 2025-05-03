# Photoalbum Railway Deploy

Ez a projekt egy Railway-en futó Django fényképalbum alkalmazás, saját MinIO (S3-kompatibilis) storage és PostgreSQL adatbázissal.

## Railway setup

1. **Új Railway projekt létrehozása**
2. **Service hozzáadása:**
   - `Django` (Python)
   - `PostgreSQL` (Railway plugin)
   - `MinIO` (Docker service, image: `minio/minio`, parancs: `server /data --console-address :9001`)
3. **MinIO bucket létrehozása:**
   - Railway MinIO konzolon hozz létre egy bucketet (pl. `photoalbum`)
4. **Environment variable-ok beállítása a Django service-hez:**
   - `DATABASE_URL` (Railway PostgreSQL pluginból)
   - `MINIO_ENDPOINT` (pl. `http://minio:9000` vagy Railway public endpoint)
   - `MINIO_ACCESS_KEY` (MinIO admin felületen generált)
   - `MINIO_SECRET_KEY` (MinIO admin felületen generált)
   - `MINIO_BUCKET_NAME` (pl. `photoalbum`)
   - `MINIO_USE_SSL` (`False` ha http, `True` ha https)
   - `SECRET_KEY` (tetszőleges erős Django secret)
   - `DEBUG` (`False` productionban)
5. **GitHub repo összekötése Railway-jel**
   - Railway automatikusan buildeli és deployolja a repót push után

## Fejlesztői futtatás

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Funkciók
- Fényképek feltöltése/törlése (csak bejelentkezett felhasználónak)
- Fényképek listázása név/dátum szerint
- Fénykép megtekintése
- Felhasználókezelés (regisztráció, belépés, kilépés)

## Megjegyzés
- A végleges beadáshoz minden Railway deploy saját MinIO-t és PostgreSQL-t használ. 