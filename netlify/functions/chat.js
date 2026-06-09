exports.handler = async function (event) {
  if (event.httpMethod !== "POST") {
    return jsonResponse(405, { error: "Method not allowed" });
  }

  const apiKey = process.env.GROQ_API_KEY;
  if (!apiKey) {
    return jsonResponse(500, {
      error: "GROQ_API_KEY is not configured for Netlify Functions.",
    });
  }

  let body;
  try {
    body = JSON.parse(event.body || "{}");
  } catch {
    return jsonResponse(400, { error: "Invalid JSON request body." });
  }

  const message = String(body.message || "").trim();
  const context = String(body.context || "").trim();

  if (!message) {
    return jsonResponse(400, { error: "Message is required." });
  }

  const systemPrompt = `You are an AI assistant for a US Disaster Dashboard.
Your goal is to help users understand the 2025 disaster projections based on the provided data context.

Rules:
1. Answer questions based on the provided context.
2. If specific data for a state is missing, provide general context about the region or common risks instead of saying you do not have that information.
3. Be concise, positive, and helpful.
4. Format your response with simple HTML tags if useful, such as <b>, <ul>, and <li>.`;

  try {
    const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: "llama-3.3-70b-versatile",
        messages: [
          { role: "system", content: systemPrompt },
          {
            role: "user",
            content: `Context:\n${context}\n\nUser Question: ${message}`,
          },
        ],
        temperature: 0.7,
        max_tokens: 500,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return jsonResponse(response.status, {
        error: data.error?.message || JSON.stringify(data),
      });
    }

    return jsonResponse(200, {
      response: data.choices?.[0]?.message?.content || "No response returned.",
    });
  } catch (error) {
    return jsonResponse(500, { error: error.message });
  }
};

function jsonResponse(statusCode, body) {
  return {
    statusCode,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  };
}

