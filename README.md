# CME-PLV (Streamlit) – Starter Project

This is a starter project for the **Cuadro de Mando Estratégico PLV** with 4 tabs:
- **Analítica (mensual)** – evolution & trends
- **Operativa (tiempo real)** – live status (placeholder, ready to connect)
- **Organizativa** – HR, training, innovation (placeholders + CSV/SQL hooks)
- **Estratégica** – balanced scorecard style KPIs & goals

## Quick start (local file demo)
1. Create a virtual env and install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run:
   ```bash
   streamlit run app.py
   ```

If you place monthly CSV/Excel files in `data/`, the app will use them. If a `.env` file exists with SQL credentials, the app will connect to SQL Server via SQLAlchemy.

## SQL setup
See `sql_examples.sql` for sample queries/views you can adapt.

## Env file
Copy `.env.example` to `.env` and fill in your SQL Server credentials to enable live queries.
