
CREATE TABLE IF NOT EXISTS batches (
    id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'PENDING',
    cs_feed_mol_m3 REAL NOT NULL DEFAULT 1.0,
    sr_feed_mol_m3 REAL NOT NULL DEFAULT 1.0,
    velocity_m_s REAL NOT NULL DEFAULT 0.001,
    bed_length_m REAL NOT NULL DEFAULT 0.1,
    frameworks TEXT NOT NULL DEFAULT '["HEU"]',
    custom_cif_name TEXT,
    custom_cif_content TEXT
);

CREATE TABLE IF NOT EXISTS subjobs (
    id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL REFERENCES batches(id) ON DELETE CASCADE,
    framework TEXT NOT NULL,
    ion TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'PENDING',
    dg_bind_kj_mol REAL,
    q_max_mol_kg REAL,
    k_langmuir_m3_mol REAL,
    removal_efficiency REAL,
    breakthrough_time_s TEXT,
    breakthrough_c TEXT,
    snapshots_json TEXT,
    mass_balance_residual REAL,
    error TEXT
);

CREATE TABLE IF NOT EXISTS batch_results (
    id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL REFERENCES batches(id) ON DELETE CASCADE,
    framework TEXT NOT NULL,
    cs_removal_efficiency REAL NOT NULL,
    sr_removal_efficiency REAL NOT NULL,
    co_capture_score REAL NOT NULL,
    rank INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS reports (
    batch_id TEXT PRIMARY KEY REFERENCES batches(id) ON DELETE CASCADE,
    report_markdown TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
