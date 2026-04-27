const BASE_URL = "https://intellex-u0y3.onrender.com";

// -------- RESEARCH --------
export async function researchCompany(company, persona, query = null) {
  try {
    const res = await fetch(`${BASE_URL}/research`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ company, persona, query }),
    });

    const data = await res.json();
    return data.result;

  } catch (err) {
    return "Error: " + err.message;
  }
}


// -------- PLANNER --------
export async function planResearch(problem) {
  try {
    const res = await fetch(`${BASE_URL}/planner`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ problem }),
    });

    const data = await res.json();
    return data.result;

  } catch (err) {
    return "Error: " + err.message;
  }
}


// -------- DOCS --------
export async function askDocs(question) {
  const res = await fetch(`${BASE_URL}/docs`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  const data = await res.json();
  return data.result;
}

import axios from "axios";

const BASE_URL = "https://intellex-u0y3.onrender.com";

export async function uploadPDF(file, onProgress) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.post(`${BASE_URL}/docs-upload-pdf`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress) {
        const percent = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        onProgress(percent);
      }
    },
  });

  return res.data.message;
}


// -------- COMPARE --------
export async function compareCompanies(c1, c2) {
  try {
    const res = await fetch(`${BASE_URL}/compare`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ company1: c1, company2: c2 }),
    });

    const data = await res.json();
    return data.result;

  } catch (err) {
    return "Error: " + err.message;
  }
}