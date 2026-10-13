import argparse
from pathlib import Path
import duckdb

def orders_report(product=None):
    # Connexion à la base DuckDB locale
    dossier = Path(__file__).resolve().parents[2]
    con = duckdb.connect(str(dossier / "analytics.duckdb"), read_only=True)

    try:
        # Calcul des commandes et des quantités par mois
        return con.execute("""
            SELECT
                strftime(date, '%Y-%m') AS month,
                COUNT(*) AS orders,
                SUM(quantity) AS quantity
            FROM orders
            WHERE $product IS NULL OR product = $product
            GROUP BY month
            ORDER BY month
        """, {"product": product}).fetchall()
    finally:
        con.close()

def main():
    # Filtre facultatif sur un produit
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--product")
    args = parser.parse_args()

    for mois, commandes, quantite in orders_report(args.product):
        print(f"{mois}\t{commandes}\t{quantite}")

if __name__ == "__main__":
    main()
