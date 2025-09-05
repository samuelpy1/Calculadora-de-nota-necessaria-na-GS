#!/usr/bin/env python3
"""
Script pro SQLite!!
"""

import os
import sqlite3


def init_database():
    db_path = "/app/data/grade_calculator.db"

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grade_calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nota_1s REAL NOT NULL,
            nota_cp_2s REAL NOT NULL,
            meta_anual REAL NOT NULL,
            nota_necessaria_gs REAL NOT NULL,
            materia TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("SELECT * FROM grade_calculations")

    if cursor.fetchone() is None:
        print("Inserindo dados de exemplo...")
        sample_data = [
            (8.0, 7.5, 8.5, 9.17, "Desenvolvimento Web"),
            (6.5, 6.0, 7.0, 7.92, "Banco de Dados"),
            (9.0, 8.5, 9.0, 9.17, "Inteligência Artificial"),
        ]

        for data in sample_data:
            cursor.execute(
                """
                INSERT OR IGNORE INTO grade_calculations 
                (nota_1s, nota_cp_2s, meta_anual, nota_necessaria_gs, materia)
                VALUES (?, ?, ?, ?, ?)
            """,
                data,
            )

        conn.commit()
        conn.close()

    print("Banco de dados inicializado com sucesso!")
    print(f"Localização: {db_path}")
    conn.close()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM grade_calculations")
    count = cursor.fetchone()[0]
    print(f"Registros na base: {count}")
    conn.close()


if __name__ == "__main__":
    init_database()
