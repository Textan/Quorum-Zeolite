
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Mutex;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProvenanceRecord {
    pub recipe_name: String,
    pub input_fingerprint: String,
    pub engine_version: String,
    pub timestamp_utc: String,
    pub host_info: String,
    pub execution_wall_time_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CachedRecipeResult {
    pub provenance: ProvenanceRecord,
    pub payload_json: String,
}

pub struct RecipeCache {
    memory_store: Mutex<HashMap<String, CachedRecipeResult>>,
}

impl RecipeCache {
    pub fn new() -> Self {
        Self {
            memory_store: Mutex::new(HashMap::new()),
        }
    }

    pub fn get(&self, key: &str) -> Option<CachedRecipeResult> {
        let store = self.memory_store.lock().ok()?;
        store.get(key).cloned()
    }

    pub fn insert(&self, key: String, result: CachedRecipeResult) {
        if let Ok(mut store) = self.memory_store.lock() {
            store.insert(key, result);
        }
    }
}
