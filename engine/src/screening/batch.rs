
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FrameworkScore {
    pub framework_name: String,
    pub iza_code: String,
    pub cs_removal_efficiency: f64,
    pub sr_removal_efficiency: f64,
    pub co_capture_score: f64,
    pub is_converged: bool,
    pub mass_balance_residual_cs: f64,
    pub mass_balance_residual_sr: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BatchLeaderboard {
    pub batch_id: String,
    pub scoring_rationale: &'static str,
    pub rankings: Vec<FrameworkScore>,
}

impl BatchLeaderboard {
    pub const SCORING_DISCLOSURE: &'static str =
        "Co-capture score is defined as min(Cs_removal, Sr_removal), penalizing frameworks that fail on either radionuclide surrogate.";

    pub fn new(batch_id: String, mut scores: Vec<FrameworkScore>) -> Self {

        scores.sort_by(|a, b| {
            b.co_capture_score
                .partial_cmp(&a.co_capture_score)
                .unwrap_or(std::cmp::Ordering::Equal)
        });

        Self {
            batch_id,
            scoring_rationale: Self::SCORING_DISCLOSURE,
            rankings: scores,
        }
    }
}
