# Quorum-Zeolite: Multiscale Physics Engine for Radionuclide Co-Capture

Quorum-Zeolite is a multiscale physics screening engine designed to evaluate crystalline zeolite frameworks (built-in IZA structures or user-uploaded CIF files) against a dual-ion $\text{Cs}^+ / \text{Sr}^{2+}$ simultaneous co-capture objective — solving the real nuclear reprocessing wastewater remediation problem (Sellafield SIXEP, Three Mile Island).

---

## Multiscale Physics Architecture

1. **Quantum Mechanical (QM) Layer (`backend/qm/`)**:
   - GFN2-xTB semi-empirical tight-binding energy evaluation per crystallographic T-site [Murthy et al. 2004, J Phys Chem B 108:2741].
   - Output: Gibbs free energy of binding $\Delta G_{\text{bind}}$ per site per ion.

2. **Isotherm Bridge (`backend/bridge/isotherm.py`)**:
   - Gaines-Thomas selectivity coefficient and single-component Langmuir affinity coupling:
     $$q = \frac{q_{\max} K C}{1 + K C}$$
     [Langmuir 1918; Gaines & Thomas 1953, J Chem Phys 21:711].

3. **Transport Layer (`backend/bridge/transport.py` & `quorum_engine`)**:
   - 1D Finite-Volume packed-bed advection-dispersion-reaction solver with Glueckauf Linear Driving Force (LDF) particle kinetics:
     $$\frac{\partial q}{\partial t} = k_{\text{LDF}} (q^* - q), \quad k_{\text{LDF}} = \frac{15 D_{\text{eff}}}{r_p^2}$$
     [Glueckauf 1955, Trans Faraday Soc 51:1540; Ruthven 1984, Ch. 8].
   - Mass balance residual check strictly enforced:
     $$\text{Mass Balance Residual} = \frac{|\text{Mass}_{\text{in}} - \text{Mass}_{\text{out}} - \text{Mass}_{\text{bed}}|}{\text{Mass}_{\text{in}}} < 1.0 \times 10^{-3}$$

4. **Co-Capture Scoring Criterion**:
   $$\text{Co-Capture Score} = \min(\eta_{\text{Cs}}, \eta_{\text{Sr}})$$
   *Deliberate scoring choice to penalize single-ion specialist materials in favor of balanced dual-capture candidates for nuclear wastewater remediation.*

---

## Running the Application

### 1. Verify Environment
```bash
bash scripts/verify_env.sh
```

### 2. Start Backend & Built-In Web Interface
```bash
# Start FastAPI backend server with rich interactive UI
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000 --reload
```
Open your browser to:
- **Batch Submission**: [http://localhost:8000/submit](http://localhost:8000/submit)
- **Interactive UI**: [http://localhost:8000](http://localhost:8000)

### 3. Optional Next.js App Router Frontend
```bash
cd frontend
npm run build && npm start
```

---

## Physical Citations

- **Ionic Radii**: Shannon (1976), *Acta Cryst A*, 32:751.
- **Hydration Enthalpy**: Marcus (1991), *Chem Rev*, 91:750.
- **Aqueous Diffusion**: Li & Gregory (1974), *Geochim Cosmochim Acta*, 38:703.
- **Coordination Numbers**: Marcus (1988), *Chem Rev*, 88:1475; Persson (2010), *Pure Appl Chem*, 82:1901.
- **LDF Kinetics**: Glueckauf (1955), *Trans Faraday Soc*, 51:1540.
- **Gaines-Thomas Exchange**: Gaines & Thomas (1953), *J Chem Phys*, 21:711.
