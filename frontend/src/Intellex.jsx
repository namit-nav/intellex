import { useState, useRef, useEffect } from "react";
import {
  researchCompany,
  planResearch,
  askDocs,
  compareCompanies,
  uploadPDF
} from "./api";


const C = {
  bg: "#06090f",
  surface: "#0d1221",
  surface2: "#121a2e",
  surface3: "#19233d",
  accent: "#f97316",
  accentSoft: "rgba(249,115,22,0.1)",
  accentBorder: "rgba(249,115,22,0.35)",
  accentGlow: "rgba(249,115,22,0.2)",
  text: "#e8edf5",
  textMuted: "#8892a4",
  textDim: "#4a5568",
  border: "rgba(255,255,255,0.05)",
  borderMid: "rgba(255,255,255,0.09)",
};

const SYSTEMS = {
  research_assistant: `You are a comprehensive business research assistant. Provide detailed, well-structured research on companies. Include: executive summary, products/services, market position, competitive landscape, recent developments, and key strategic insights. Use clear section headers with ##.`,
  market_analyst: `You are an expert market analyst. Analyze companies with focus on market positioning, growth vectors, competitive dynamics, addressable market, and investment considerations. Be analytical and data-driven. Use clear section headers with ##.`,
  sales_strategist: `You are a strategic sales intelligence advisor. Research companies focusing on: key decision makers, organizational pain points, budget signals, tech stack, recent strategic initiatives, and actionable outreach angles. Use clear section headers with ##.`,
};


function Spinner() {
  return (
    <span style={{
      display: "inline-block", width: 18, height: 18,
      border: `2px solid ${C.surface3}`,
      borderTop: `2px solid ${C.accent}`,
      borderRadius: "50%",
      animation: "spin 0.7s linear infinite",
    }} />
  );
}

function Tag({ children, color }) {
  return (
    <span style={{
      fontSize: 11, fontWeight: 600, letterSpacing: "0.08em",
      textTransform: "uppercase", padding: "3px 8px",
      borderRadius: 4, background: color || C.accentSoft,
      color: color ? "#fff" : C.accent, border: `1px solid ${color || C.accentBorder}`,
    }}>{children}</span>
  );
}

function ReportDisplay({ text }) {
  const lines = text.split("\n");
  return (
    <div style={{ lineHeight: 1.75, color: C.text }}>
      {lines.map((line, i) => {
        if (line.startsWith("## ")) return (
          <h3 key={i} style={{ color: C.accent, fontSize: 13, fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase", margin: "24px 0 8px", borderBottom: `1px solid ${C.accentBorder}`, paddingBottom: 6 }}>
            {line.slice(3)}
          </h3>
        );
        if (line.startsWith("**") && line.endsWith("**")) return (
          <p key={i} style={{ fontWeight: 600, color: C.text, margin: "8px 0 4px" }}>{line.slice(2, -2)}</p>
        );
        if (line.startsWith("- ")) return (
          <div key={i} style={{ display: "flex", gap: 10, margin: "4px 0" }}>
            <span style={{ color: C.accent, marginTop: 2, flexShrink: 0 }}>›</span>
            <span style={{ color: C.textMuted, fontSize: 14 }}>{line.slice(2)}</span>
          </div>
        );
        if (line.trim() === "") return <div key={i} style={{ height: 8 }} />;
        return <p key={i} style={{ color: C.textMuted, fontSize: 14, margin: "4px 0" }}>{line}</p>;
      })}
    </div>
  );
}

function LoginScreen({ onLogin }) {
  const [pw, setPw] = useState("");
  const [err, setErr] = useState(false);
  const [shake, setShake] = useState(false);

  const attempt = () => {
    if (pw === "duckcoders123") {
      onLogin();
    } else {
      setErr(true);
      setShake(true);
      setTimeout(() => setShake(false), 500);
    }
  };

  return (
    <div style={{
      minHeight: "100vh", background: C.bg,
      display: "flex", flexDirection: "column",
      alignItems: "center", justifyContent: "center",
      fontFamily: "'SF Pro Display', -apple-system, 'Segoe UI', sans-serif",
    }}>
      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes shake { 0%,100%{transform:translateX(0)} 20%,60%{transform:translateX(-8px)} 40%,80%{transform:translateX(8px)} }
        @keyframes fadeUp { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
        @keyframes scanline { 0%{transform:translateY(-100%)} 100%{transform:translateY(100vh)} }
      `}</style>

      <div style={{
        position: "absolute", top: 0, left: 0, right: 0, bottom: 0,
        background: `radial-gradient(ellipse 60% 50% at 50% 0%, rgba(249,115,22,0.08) 0%, transparent 70%)`,
        pointerEvents: "none",
      }} />

      <div style={{
        animation: "fadeUp 0.6s ease forwards",
        width: 360, padding: "48px 40px",
        background: C.surface,
        border: `1px solid ${C.border}`,
        borderRadius: 16,
        boxShadow: `0 0 60px rgba(249,115,22,0.08), 0 24px 48px rgba(0,0,0,0.5)`,
      }}>
        <div style={{ textAlign: "center", marginBottom: 40 }}>
          <div style={{ fontSize: 28, fontWeight: 800, letterSpacing: "-0.5px", color: C.text, marginBottom: 6 }}>
            INTEL<span style={{ color: C.accent }}>EX</span>
          </div>
          <div style={{ fontSize: 12, color: C.textDim, letterSpacing: "0.2em", textTransform: "uppercase" }}>
            Research Intelligence Platform
          </div>
        </div>

        <div style={{
          animation: shake ? "shake 0.4s ease" : "none",
        }}>
          <label style={{ fontSize: 11, color: C.textDim, letterSpacing: "0.12em", textTransform: "uppercase", display: "block", marginBottom: 8 }}>
            Access Code
          </label>
          <input
            type="password"
            value={pw}
            onChange={(e) => { setPw(e.target.value); setErr(false); }}
            onKeyDown={(e) => e.key === "Enter" && attempt()}
            placeholder="Enter password"
            style={{
              width: "100%", padding: "12px 16px", fontSize: 15,
              background: C.surface2, border: `1px solid ${err ? "rgba(239,68,68,0.5)" : C.borderMid}`,
              borderRadius: 8, color: C.text, outline: "none",
              boxSizing: "border-box", letterSpacing: "0.05em",
              transition: "border 0.2s",
            }}
          />
          {err && <div style={{ fontSize: 12, color: "#ef4444", marginTop: 8 }}>Incorrect access code</div>}
        </div>

        <button
          onClick={attempt}
          style={{
            width: "100%", marginTop: 20, padding: "13px",
            background: C.accent, border: "none", borderRadius: 8,
            color: "#fff", fontSize: 14, fontWeight: 700,
            letterSpacing: "0.08em", textTransform: "uppercase",
            cursor: "pointer", transition: "opacity 0.2s",
          }}
          onMouseEnter={(e) => e.target.style.opacity = "0.85"}
          onMouseLeave={(e) => e.target.style.opacity = "1"}
        >
          Authenticate
        </button>
      </div>

      <div style={{ marginTop: 24, fontSize: 11, color: C.textDim, letterSpacing: "0.15em" }}>
        © INTELLEX RESEARCH
      </div>
    </div>
  );
}

function NavBar({ page, setPage, onLogout }) {
  const navItems = ["About", "Tools", "Contact"];
  return (
    <div style={{
      display: "flex", alignItems: "center", justifyContent: "space-between",
      padding: "0 32px", height: 60,
      background: C.surface,
      borderBottom: `1px solid ${C.border}`,
      position: "sticky", top: 0, zIndex: 100,
    }}>
      <div style={{ fontSize: 20, fontWeight: 800, letterSpacing: "-0.5px", color: C.text }}>
        INTEL<span style={{ color: C.accent }}>EX</span>
        <span style={{ fontSize: 10, color: C.textDim, fontWeight: 400, marginLeft: 10, letterSpacing: "0.15em", textTransform: "uppercase" }}>Intelligence</span>
      </div>

      <div style={{ display: "flex", gap: 4, alignItems: "center" }}>
        {navItems.map((item) => (
          <button key={item} onClick={() => setPage(item)}
            style={{
              padding: "7px 16px", background: "transparent",
              border: "none", borderRadius: 6,
              color: page === item ? C.text : C.textMuted,
              fontSize: 13, fontWeight: page === item ? 600 : 400,
              cursor: "pointer",
              borderBottom: page === item ? `2px solid ${C.accent}` : "2px solid transparent",
              transition: "all 0.2s",
            }}>{item}</button>
        ))}
        <div style={{ width: 1, height: 20, background: C.border, margin: "0 8px" }} />
        <button onClick={onLogout} style={{
          padding: "6px 14px",
          background: "transparent",
          border: `1px solid ${C.accentBorder}`,
          borderRadius: 6, color: C.accent,
          fontSize: 12, fontWeight: 600, cursor: "pointer",
          transition: "all 0.2s",
        }}
          onMouseEnter={(e) => { e.currentTarget.style.background = C.accentSoft; }}
          onMouseLeave={(e) => { e.currentTarget.style.background = "transparent"; }}
        >
          Logout
        </button>
      </div>
    </div>
  );
}

function Card({ children, style }) {
  return (
    <div style={{
      background: C.surface, border: `1px solid ${C.border}`,
      borderRadius: 12, padding: 24, ...style,
    }}>{children}</div>
  );
}

function Input({ label, value, onChange, placeholder, type = "text" }) {
  return (
    <div style={{ marginBottom: 16 }}>
      {label && <label style={{ fontSize: 11, color: C.textDim, letterSpacing: "0.12em", textTransform: "uppercase", display: "block", marginBottom: 6 }}>{label}</label>}
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        style={{
          width: "100%", padding: "10px 14px", fontSize: 14,
          background: C.surface2, border: `1px solid ${C.borderMid}`,
          borderRadius: 8, color: C.text, outline: "none",
          boxSizing: "border-box",
          transition: "border 0.2s",
        }}
        onFocus={(e) => e.target.style.borderColor = C.accentBorder}
        onBlur={(e) => e.target.style.borderColor = C.borderMid}
      />
    </div>
  );
}

function Select({ label, value, onChange, options }) {
  return (
    <div style={{ marginBottom: 16 }}>
      {label && <label style={{ fontSize: 11, color: C.textDim, letterSpacing: "0.12em", textTransform: "uppercase", display: "block", marginBottom: 6 }}>{label}</label>}
      <select value={value} onChange={(e) => onChange(e.target.value)} style={{
        width: "100%", padding: "10px 14px", fontSize: 14,
        background: C.surface2, border: `1px solid ${C.borderMid}`,
        borderRadius: 8, color: C.text, outline: "none",
        boxSizing: "border-box", cursor: "pointer",
        appearance: "none",
      }}>
        {options.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
      </select>
    </div>
  );
}

function PrimaryButton({ children, onClick, loading, disabled, style }) {
  return (
    <button
      onClick={onClick}
      disabled={loading || disabled}
      style={{
        padding: "11px 24px", background: loading || disabled ? C.surface3 : C.accent,
        border: "none", borderRadius: 8, color: loading || disabled ? C.textMuted : "#fff",
        fontSize: 13, fontWeight: 700, letterSpacing: "0.06em", textTransform: "uppercase",
        cursor: loading || disabled ? "not-allowed" : "pointer",
        display: "inline-flex", alignItems: "center", gap: 8,
        transition: "all 0.2s", ...style,
      }}
      onMouseEnter={(e) => { if (!loading && !disabled) e.currentTarget.style.opacity = "0.85"; }}
      onMouseLeave={(e) => { e.currentTarget.style.opacity = "1"; }}
    >
      {loading && <Spinner />}
      {children}
    </button>
  );
}

function ResearchTool() {
  const [company, setCompany] = useState("");
  const [persona, setPersona] = useState("research_assistant");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [chatInput, setChatInput] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [chatLoading, setChatLoading] = useState(false);

  const generate = async () => {
    if (!company.trim()) return;
    setLoading(true);
    setReport(null);
    setChatHistory([]);
    
    try {
      const result = await researchCompany(company, persona);
      setReport(result);
    } catch (err) {
      setReport("Failed to fetch report");
    }
    
    setLoading(false);
  };

  const sendChat = async () => {
    if (!chatInput.trim() || !report) return;
    const msg = chatInput;
    setChatInput("");
    setChatLoading(true);
    
    const newHistory = [...chatHistory, { role: "user", content: msg }];
    setChatHistory(newHistory);
    try {
      const response = await researchCompany(company, persona, msg);
      setChatHistory([
        ...newHistory,
        { role: "assistant", content: response }
      ]);
    } catch (err) {
      setChatHistory([
        ...newHistory,
        { role: "assistant", content: "Error getting response" }
      ]);
    }
    setChatLoading(false);
  };

  const downloadPDF = async () => {
    console.log("REPORT:", report);
  try {
    const res = await fetch("https://intellex-u0y3.onrender.com/export-pdf", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        content: report,
      }),
    });

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `${company}-report.pdf`;
    a.click();
  } catch (err) {
    console.error(err);
    alert("PDF download failed");
  }
};

  return (
    <div>
      <Card>
        <div style={{ display: "flex", gap: 12, alignItems: "flex-end", flexWrap: "wrap" }}>
          <div style={{ flex: 2, minWidth: 200 }}>
            <Input label="Company Name" value={company} onChange={setCompany} placeholder="e.g. OpenAI, Tesla, Stripe..." />
          </div>
          <div style={{ flex: 1, minWidth: 180 }}>
            <Select label="Analysis Persona" value={persona} onChange={setPersona} options={[
              { value: "research_assistant", label: "Research Assistant" },
              { value: "market_analyst", label: "Market Analyst" },
              { value: "sales_strategist", label: "Sales Strategist" },
            ]} />
          </div>
          <div style={{ marginBottom: 16 }}>
            <PrimaryButton onClick={generate} loading={loading} disabled={!company.trim()}>
              {loading ? "Researching..." : "Generate Report"}
            </PrimaryButton>
          </div>
        </div>
      </Card>

      {loading && (
        <Card style={{ marginTop: 16, textAlign: "center", padding: "48px 24px" }}>
          <div style={{ marginBottom: 12 }}><Spinner /></div>
          <div style={{ color: C.textMuted, fontSize: 14 }}>Analyzing {company}...</div>
          <div style={{ color: C.textDim, fontSize: 12, marginTop: 6 }}>Gathering intelligence from multiple sources</div>
        </Card>
      )}

      {report && (
        <>
          <Card style={{ marginTop: 16 }}>
            <div style={{ marginBottom: 12 }}>
              <button
              onClick={downloadPDF}
              style={{
                padding: "8px 14px",
                background: "#f97316",
                border: "none",
                borderRadius: 6,
                color: "#fff",
                fontSize: 12,
                fontWeight: 600,
                cursor: "pointer"
              }}
              >
                Download PDF
              </button>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
              <div>
                <div style={{ fontSize: 16, fontWeight: 700, color: C.text }}>{company}</div>
                <div style={{ fontSize: 12, color: C.textDim, marginTop: 2 }}>
                  <Tag>{persona.replace("_", " ")}</Tag>
                </div>
              </div>
            </div>
            <ReportDisplay text={report} />
          </Card>

          <Card style={{ marginTop: 16 }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: C.text, marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
              <span style={{ color: C.accent }}>◈</span> Follow-up Chat
            </div>

            {chatHistory.map((msg, i) => (
              <div key={i} style={{
                display: "flex", gap: 10, marginBottom: 12,
                flexDirection: msg.role === "user" ? "row-reverse" : "row",
              }}>
                <div style={{
                  width: 28, height: 28, borderRadius: "50%", flexShrink: 0,
                  background: msg.role === "user" ? C.accentSoft : C.surface2,
                  border: `1px solid ${msg.role === "user" ? C.accentBorder : C.borderMid}`,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontSize: 11, fontWeight: 700,
                  color: msg.role === "user" ? C.accent : C.textMuted,
                }}>
                  {msg.role === "user" ? "U" : "AI"}
                </div>
                <div style={{
                  maxWidth: "75%", padding: "10px 14px", borderRadius: 8, fontSize: 13, lineHeight: 1.6,
                  background: msg.role === "user" ? C.accentSoft : C.surface2,
                  border: `1px solid ${msg.role === "user" ? C.accentBorder : C.borderMid}`,
                  color: C.text,
                }}>
                  {msg.content}
                </div>
              </div>
            ))}

            {chatLoading && (
              <div style={{ display: "flex", gap: 10, marginBottom: 12 }}>
                <div style={{ width: 28, height: 28, borderRadius: "50%", background: C.surface2, border: `1px solid ${C.borderMid}`, display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <Spinner />
                </div>
                <div style={{ padding: "10px 14px", background: C.surface2, borderRadius: 8, color: C.textMuted, fontSize: 13 }}>
                  <span style={{ animation: "pulse 1.5s ease infinite", display: "inline-block" }}>Thinking...</span>
                </div>
              </div>
            )}

            <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
              <input
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && sendChat()}
                placeholder="Ask a follow-up question..."
                style={{
                  flex: 1, padding: "10px 14px", fontSize: 13,
                  background: C.surface2, border: `1px solid ${C.borderMid}`,
                  borderRadius: 8, color: C.text, outline: "none",
                }}
                onFocus={(e) => e.target.style.borderColor = C.accentBorder}
                onBlur={(e) => e.target.style.borderColor = C.borderMid}
              />
              <PrimaryButton onClick={sendChat} loading={chatLoading} disabled={!chatInput.trim()}>
                Send
              </PrimaryButton>
            </div>
          </Card>
        </>
      )}
    </div>
  );
}

function PlannerTool() {
  const [problem, setProblem] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!problem.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await planResearch(problem);
      setResult(res);
    } catch (err) {
      setResult("Error generating plan");
    }
    setLoading(false);
  };

  return (
    <div>
      <Card>
        <div style={{ marginBottom: 16 }}>
          <label style={{ fontSize: 11, color: C.textDim, letterSpacing: "0.12em", textTransform: "uppercase", display: "block", marginBottom: 8 }}>
            Problem or Goal
          </label>
          <textarea
            value={problem}
            onChange={(e) => setProblem(e.target.value)}
            placeholder="Describe the problem, challenge, or goal you want a plan for..."
            rows={4}
            style={{
              width: "100%", padding: "12px 14px", fontSize: 14,
              background: C.surface2, border: `1px solid ${C.borderMid}`,
              borderRadius: 8, color: C.text, outline: "none",
              boxSizing: "border-box", resize: "vertical", lineHeight: 1.6,
              fontFamily: "inherit",
            }}
            onFocus={(e) => e.target.style.borderColor = C.accentBorder}
            onBlur={(e) => e.target.style.borderColor = C.borderMid}
          />
        </div>
        <PrimaryButton onClick={generate} loading={loading} disabled={!problem.trim()}>
          {loading ? "Planning..." : "Generate Plan"}
        </PrimaryButton>
      </Card>

      {loading && (
        <Card style={{ marginTop: 16, textAlign: "center", padding: "48px 24px" }}>
          <div style={{ marginBottom: 12 }}><Spinner /></div>
          <div style={{ color: C.textMuted, fontSize: 14 }}>Building your strategic plan...</div>
        </Card>
      )}

      {result && (
        <Card style={{ marginTop: 16 }}>
          <div style={{ fontSize: 13, fontWeight: 600, color: C.text, marginBottom: 20, display: "flex", alignItems: "center", gap: 8 }}>
            <span style={{ color: C.accent }}>◈</span> Strategic Plan
          </div>
          <ReportDisplay text={result} />
        </Card>
      )}
    </div>
  );
}

function DocsTool() {
  const [docContent, setDocContent] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const fileRef = useRef();

  // -------- HANDLE PDF UPLOAD --------
  const handleFile = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      const msg = await uploadPDF(file);
      alert(msg);
      setUploaded(true);        
      setDocContent("");        
    } catch (err) {
      alert("Upload failed");
    }
  };

  // -------- ASK QUESTION --------
  const ask = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer(null);

    try {
      const res = await askDocs(question);
      setAnswer(res);
    } catch (err) {
      setAnswer("Error analyzing document");
    }

    setLoading(false);
  };

  return (
    <div>
      <Card>
        <div style={{ marginBottom: 16 }}>
          <div
            style={{
              fontSize: 11,
              color: C.textDim,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              marginBottom: 8,
            }}
          >
            Document
          </div>

          {/* -------- Upload Section -------- */}
          <div style={{ display: "flex", gap: 8, marginBottom: 10 }}>
            <button
              onClick={() => fileRef.current.click()}
              style={{
                padding: "9px 16px",
                background: C.surface2,
                border: `1px solid ${C.borderMid}`,
                borderRadius: 8,
                color: C.textMuted,
                fontSize: 13,
                cursor: "pointer",
              }}
            >
              Upload PDF
            </button>

            <input
              ref={fileRef}
              type="file"
              accept=".pdf"
              onChange={handleFile}
              style={{ display: "none" }}
            />

            {uploaded && (
              <Tag color="rgba(34,197,94,0.25)">PDF loaded</Tag>
            )}
          </div>

          {/* -------- Optional Text Input -------- */}
          <div
            style={{
              fontSize: 12,
              color: C.textDim,
              marginBottom: 8,
            }}
          >
            (Optional) Paste document content directly:
          </div>

          <textarea
            value={docContent}
            onChange={(e) => setDocContent(e.target.value)}
            placeholder="Paste text if not using PDF..."
            rows={6}
            style={{
              width: "100%",
              padding: "12px 14px",
              fontSize: 13,
              background: C.surface2,
              border: `1px solid ${C.borderMid}`,
              borderRadius: 8,
              color: C.text,
              outline: "none",
              boxSizing: "border-box",
              resize: "vertical",
              lineHeight: 1.6,
              fontFamily: "monospace",
            }}
            onFocus={(e) => (e.target.style.borderColor = C.accentBorder)}
            onBlur={(e) => (e.target.style.borderColor = C.borderMid)}
          />

          <div
            style={{
              fontSize: 11,
              color: C.textDim,
              marginTop: 4,
            }}
          >
            {docContent.length} characters
          </div>
        </div>

        {/* -------- Question Input -------- */}
        <div style={{ display: "flex", gap: 8 }}>
          <div style={{ flex: 1 }}>
            <Input
              label="Your Question"
              value={question}
              onChange={setQuestion}
              placeholder="What does the document say about..."
            />
          </div>
        </div>

        {/* -------- Ask Button -------- */}
        <PrimaryButton
          onClick={ask}
          loading={loading}
          disabled={!question.trim()}
        >
          {loading ? "Analyzing..." : "Ask Question"}
        </PrimaryButton>
      </Card>

      {/* -------- Loading -------- */}
      {loading && (
        <Card
          style={{
            marginTop: 16,
            textAlign: "center",
            padding: "40px 24px",
          }}
        >
          <div style={{ marginBottom: 12 }}>
            <Spinner />
          </div>
          <div style={{ color: C.textMuted, fontSize: 14 }}>
            Reading document...
          </div>
        </Card>
      )}

      {/* -------- Answer -------- */}
      {answer && (
        <Card style={{ marginTop: 16 }}>
          <div
            style={{
              fontSize: 13,
              fontWeight: 600,
              color: C.text,
              marginBottom: 16,
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span style={{ color: C.accent }}>◈</span> Answer
          </div>

          <div
            style={{
              fontSize: 12,
              color: C.textDim,
              marginBottom: 12,
              padding: "8px 12px",
              background: C.surface2,
              borderRadius: 6,
              borderLeft: `3px solid ${C.accentBorder}`,
            }}
          >
            Q: {question}
          </div>

          <ReportDisplay text={answer} />
        </Card>
      )}
    </div>
  );
}

function CompareTool() {
  const [c1, setC1] = useState("");
  const [c2, setC2] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const compare = async () => {
    if (!c1.trim() || !c2.trim()) return;
    setLoading(true);
    setResult(null);
    setStatus("Comparing companies...");
    try {
      const res = await compareCompanies(c1, c2);
      setResult(res);
    } catch (err) {
      setResult("Error comparing companies");
    }
    setStatus("");
    setLoading(false);
  };

  return (
    <div>
      <Card>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 40px 1fr", gap: 8, alignItems: "center", marginBottom: 16 }}>
          <div>
            <Input label="Company A" value={c1} onChange={setC1} placeholder="First company..." />
          </div>
          <div style={{ textAlign: "center", color: C.textDim, fontSize: 18, fontWeight: 700, paddingTop: 4 }}>vs</div>
          <div>
            <Input label="Company B" value={c2} onChange={setC2} placeholder="Second company..." />
          </div>
        </div>
        <PrimaryButton onClick={compare} loading={loading} disabled={!c1.trim() || !c2.trim()}>
          {loading ? status || "Comparing..." : "Compare Companies"}
        </PrimaryButton>
      </Card>

      {loading && (
        <Card style={{ marginTop: 16, textAlign: "center", padding: "48px 24px" }}>
          <div style={{ marginBottom: 12 }}><Spinner /></div>
          <div style={{ color: C.textMuted, fontSize: 14 }}>{status}</div>
          <div style={{ color: C.textDim, fontSize: 12, marginTop: 6 }}>This may take a moment — researching both companies</div>
        </Card>
      )}

      {result && (
        <Card style={{ marginTop: 16 }}>
          <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 20, paddingBottom: 16, borderBottom: `1px solid ${C.border}` }}>
            <div style={{ flex: 1, textAlign: "center" }}>
              <div style={{ fontSize: 16, fontWeight: 700, color: C.text }}>{c1}</div>
              <Tag>Company A</Tag>
            </div>
            <div style={{ color: C.textDim, fontSize: 20, fontWeight: 700 }}>vs</div>
            <div style={{ flex: 1, textAlign: "center" }}>
              <div style={{ fontSize: 16, fontWeight: 700, color: C.text }}>{c2}</div>
              <Tag color="rgba(59,130,246,0.2)">Company B</Tag>
            </div>
          </div>
          <ReportDisplay text={result} />
        </Card>
      )}
    </div>
  );
}

const TOOLS = [
  { id: "Research", icon: "⬡", label: "Research", desc: "Deep company intelligence reports" },
  { id: "Planner", icon: "◫", label: "Planner", desc: "Strategic planning & roadmaps" },
  { id: "Docs", icon: "▣", label: "Docs", desc: "Document analysis & Q&A" },
  { id: "Compare", icon: "⇌", label: "Compare", desc: "Side-by-side company comparison" },
];

function ToolsPage() {
  const [activeTool, setActiveTool] = useState(null);
  return (
    <div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 24 }}>
        {TOOLS.map((t) => (
          <button key={t.id} onClick={() => setActiveTool(t.id)} style={{
            background: activeTool === t.id ? C.accentSoft : C.surface,
            border: `1px solid ${activeTool === t.id ? C.accentBorder : C.border}`,
            borderRadius: 10, padding: "18px 16px",
            cursor: "pointer", textAlign: "left",
            transition: "all 0.2s",
            boxShadow: activeTool === t.id ? `0 0 20px ${C.accentGlow}` : "none",
          }}
            onMouseEnter={(e) => { if (activeTool !== t.id) { e.currentTarget.style.borderColor = C.borderMid; e.currentTarget.style.background = C.surface2; } }}
            onMouseLeave={(e) => { if (activeTool !== t.id) { e.currentTarget.style.borderColor = C.border; e.currentTarget.style.background = C.surface; } }}
          >
            <div style={{ fontSize: 22, marginBottom: 8, color: activeTool === t.id ? C.accent : C.textDim }}>{t.icon}</div>
            <div style={{ fontSize: 14, fontWeight: 600, color: activeTool === t.id ? C.text : C.textMuted, marginBottom: 4 }}>{t.label}</div>
            <div style={{ fontSize: 11, color: C.textDim, lineHeight: 1.4 }}>{t.desc}</div>
          </button>
        ))}
      </div>

      {activeTool === "Research" && <ResearchTool />}
      {activeTool === "Planner" && <PlannerTool />}
      {activeTool === "Docs" && <DocsTool />}
      {activeTool === "Compare" && <CompareTool />}

      {!activeTool && (
        <div style={{ textAlign: "center", padding: "60px 0", color: C.textDim }}>
          <div style={{ fontSize: 40, marginBottom: 12, opacity: 0.3 }}>◈</div>
          <div style={{ fontSize: 14 }}>Select a tool above to get started</div>
        </div>
      )}
    </div>
  );
}

function AboutPage() {
  const features = [
    { icon: "⬡", title: "Company Research", desc: "Deep-dive intelligence reports powered by AI, customizable by analyst persona." },
    { icon: "◫", title: "Strategic Planner", desc: "Transform problems into structured action plans with milestones and risk analysis." },
    { icon: "▣", title: "Document Analysis", desc: "Upload or paste documents and get precise, contextual answers instantly." },
    { icon: "⇌", title: "Company Comparison", desc: "Side-by-side competitive analysis with balanced, data-grounded insights." },
  ];

  return (
    <div>
      <div style={{
        padding: "48px 0 32px",
        borderBottom: `1px solid ${C.border}`,
        marginBottom: 32,
      }}>
        <div style={{ fontSize: 11, color: C.accent, letterSpacing: "0.2em", textTransform: "uppercase", marginBottom: 12 }}>
          Research Intelligence Platform
        </div>
        <h1 style={{ fontSize: 36, fontWeight: 800, color: C.text, margin: "0 0 16px", letterSpacing: "-1px", lineHeight: 1.2 }}>
          AI-powered research,<br />
          <span style={{ color: C.accent }}>at your fingertips.</span>
        </h1>
        <p style={{ fontSize: 15, color: C.textMuted, maxWidth: 520, lineHeight: 1.7, margin: 0 }}>
          Intellex combines advanced AI with structured research frameworks to deliver actionable intelligence for companies, markets, and documents.
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 16 }}>
        {features.map((f) => (
          <Card key={f.title} style={{ display: "flex", gap: 16, alignItems: "flex-start" }}>
            <div style={{ fontSize: 24, color: C.accent, flexShrink: 0 }}>{f.icon}</div>
            <div>
              <div style={{ fontSize: 14, fontWeight: 700, color: C.text, marginBottom: 6 }}>{f.title}</div>
              <div style={{ fontSize: 13, color: C.textMuted, lineHeight: 1.6 }}>{f.desc}</div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

function ContactPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [sent, setSent] = useState(false);

  const send = () => {
    if (name && email && message) setSent(true);
  };

  if (sent) return (
    <Card style={{ textAlign: "center", padding: "64px 32px" }}>
      <div style={{ fontSize: 36, marginBottom: 16, color: C.accent }}>✓</div>
      <div style={{ fontSize: 18, fontWeight: 700, color: C.text, marginBottom: 8 }}>Message Sent</div>
      <div style={{ fontSize: 14, color: C.textMuted }}>We'll be in touch at {email}</div>
    </Card>
  );

  return (
    <div style={{ maxWidth: 520 }}>
      <div style={{ marginBottom: 32 }}>
        <h2 style={{ fontSize: 24, fontWeight: 800, color: C.text, margin: "0 0 8px" }}>Get in Touch</h2>
        <p style={{ fontSize: 14, color: C.textMuted, margin: 0 }}>support@intellex.ai</p>
      </div>
      <Card>
        <Input label="Name" value={name} onChange={setName} placeholder="Your name" />
        <Input label="Email" value={email} onChange={setEmail} placeholder="you@company.com" type="email" />
        <div style={{ marginBottom: 16 }}>
          <label style={{ fontSize: 11, color: C.textDim, letterSpacing: "0.12em", textTransform: "uppercase", display: "block", marginBottom: 6 }}>Message</label>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="How can we help?"
            rows={5}
            style={{
              width: "100%", padding: "12px 14px", fontSize: 14,
              background: C.surface2, border: `1px solid ${C.borderMid}`,
              borderRadius: 8, color: C.text, outline: "none",
              boxSizing: "border-box", resize: "vertical", lineHeight: 1.6, fontFamily: "inherit",
            }}
            onFocus={(e) => e.target.style.borderColor = C.accentBorder}
            onBlur={(e) => e.target.style.borderColor = C.borderMid}
          />
        </div>
        <PrimaryButton onClick={send} disabled={!name || !email || !message}>Send Message</PrimaryButton>
      </Card>
    </div>
  );
}

export default function Intellex() {
  const [auth, setAuth] = useState(false);
  const [page, setPage] = useState("About");

  if (!auth) return <LoginScreen onLogin={() => setAuth(true)} />;

  return (
    <div style={{
      minHeight: "100vh",
      background: C.bg,
      fontFamily: "'SF Pro Display', -apple-system, 'Segoe UI', BlinkMacSystemFont, sans-serif",
      color: C.text,
    }}>
      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes fadeUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
        input::placeholder, textarea::placeholder { color: #3a4a60; }
        select option { background: #0d1221; }
      `}</style>

      <NavBar page={page} setPage={setPage} onLogout={() => { setAuth(false); setPage("About"); }} />

      <div style={{ maxWidth: 960, margin: "0 auto", padding: "32px 24px", animation: "fadeUp 0.4s ease" }}>
        {page === "About" && <AboutPage />}
        {page === "Tools" && <ToolsPage />}
        {page === "Contact" && <ContactPage />}
      </div>

      <div style={{ textAlign: "center", padding: "32px", borderTop: `1px solid ${C.border}`, marginTop: 48, fontSize: 11, color: C.textDim, letterSpacing: "0.1em" }}>
        © INTELLEX RESEARCH · AI-POWERED INTELLIGENCE PLATFORM
      </div>
    </div>
  );
}
