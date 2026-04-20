const BASE_URL = "http://127.0.0.1:8000";

export async function researchCompany(company, persona) {
  const res = await fetch(`${BASE_URL}/research`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ company, persona }),
  });

  return await res.json();
}

export async function planResearch(problem) {
  const res = await fetch(`${BASE_URL}/planner`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ problem }),
  });

  return await res.json();
}

export async function askDocs(question, content) {
  const res = await fetch(`${BASE_URL}/docs`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question, content }),
  });

  return await res.json();
}

export async function compareCompanies(c1, c2) {
  const res = await fetch(`${BASE_URL}/compare`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ company1: c1, company2: c2 }),
  });

  return await res.json();
}