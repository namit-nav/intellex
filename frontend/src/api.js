const BASE_URL = "http://127.0.0.1:8000";

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
export async function askDocs(question, content) {
  try {
    const res = await fetch(`${BASE_URL}/docs`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question, content }),
    });

    const data = await res.json();
    return data.result;

  } catch (err) {
    return "Error: " + err.message;
  }
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