import sqlite3

# Charger l'extension Spatialite
def check_spatialite():
    try:
        with sqlite3.connect(':memory:') as db:
            db.enable_load_extension(True)
            db.execute("SELECT load_extension('mod_spatialite');")
            version = db.execute("SELECT spatialite_version();").fetchone()[0]
            print(f"Spatialite version: {version}")
    except Exception as e:
        print(f"Erreur lors du chargement de Spatialite : {e}")

if __name__ == "__main__":
    check_spatialite()
