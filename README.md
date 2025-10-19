# ExpansionRx-Challenge-Tutorial
[![Logo](https://img.shields.io/badge/OSMF-OpenADMET-%23002f4a)](https://openadmet.org/)

This repo provides a guide and example workflows to participate in the [**ExpansionRx-OpenADMET Blind Challenge**](https://openadmet.ghost.io/expansionrx-openadmet-blind-challenge/), a community-driven initiative to benchmark models for predicting **ADMET** (Absorption, Distribution, Metabolism, Excretion, Toxicity) properties in drug discovery on a unique real world dataset.

In the tutorial notebook you will find an example workflow to train a simple set of models using the provided training data, and generate predictions for submission to the challenge platform on [Hugging Face](https://huggingface.co/spaces/openadmet/OpenADMET-ExpansionRx-Challenge).

We have a dedicated [Discord server](https://discord.gg/FeSZCTf5sa) for Q&A, discussion, and support during the challenge. Our evaluation logic is also open source and available on in this repo. We welcome feedback and community discussion on all aspects the challenge!

---

## 🧪 About the Challenge

Participants are tasked with predicting 9 ADMET endpoints for small molecules using real-world drug discovery data provided by **ExpansionRx**.

**Endpoints:**
- LogD  
- Kinetic Solubility (**KSol**)  
- Mouse Liver Microsomal Clearance (**MLM CLint**)  
- Human Liver Microsomal Clearance (**HLM CLint**)  
- Caco-2 Efflux Ratio  
- Caco-2 Permeability (Papp A>B)  
- Mouse Plasma Protein Binding (**MPPB**)  
- Mouse Brain Protein Binding (**MBPB**)  
- Mouse Gastrocnemius Muscle Binding (**MGMB**)

More details on endpoints: [Blog Post](https://openadmet.ghost.io/openadmet-expansionrx-blind-challenge/)

---

## 📦 Dataset

- **Training Data**:  
  Available on [Hugging Face](https://huggingface.co/datasets/openadmet/openadmet-expansionrx-challenge-train-data)  
  Includes SMILES and ADMET measurements for a series of molecules.

- **Test Data**:  
  Blinded — predictions must be submitted to the challenge platform. Blinded test data also available on [HuggingFace](https://huggingface.co/datasets/openadmet/openadmet-expansionrx-challenge-test-data-blinded)

---

## ✅ How to Participate

1. **Follow the tutorial**  via this repo to learn about the submission process.
2. **Download** the public dataset.
3. **Train** your model on any or all endpoints.
4. **Submit** predictions to the [challenge platform](https://huggingface.co/spaces/openadmet/OpenADMET-ExpansionRx-Challenge) (1 per day max, latest counts).
5. Join the [Discord](https://discord.gg/FeSZCTf5sa) for Q&A and support.

---

## 🏆 Evaluation

- Scored using **Mean Absolute Error (MAE)** per endpoint.
- Overall ranking by **Macro-Averaged Relative Absolute Error (MA-RAE)**.
- Submissions may include external data or pretraining.
- Submissions can be anonymous if desired
- Winners announced January 26, 2026.
---

## 📅 Key Dates

- 🗓 **Challenge Starts**: October 27, 2025  
- ⏳ **Submission Deadline**: January 19, 2026  
- 🏁 **Winners Announced**: January 26, 2026  
