const API = "http://localhost:5001"; //host ip:port

async function getPlaces() {
  try {
    const res = await fetch(`${API}/places`);
    const data = await res.json();
    const ul = document.getElementById("places");
    ul.innerHTML = "";
    data.forEach(p => {
      const li = document.createElement("li");
      li.textContent = `${p.name} - ${p.location}`;
      ul.appendChild(li);
    });
  } catch (err) {
    console.error("Fetch GET error:", err);
  }
}

async function addPlace() {
  const name = document.getElementById("name").value;
  const location = document.getElementById("location").value;
  if (!name || !location) return alert("Please fill in both fields.");

  try {
    await fetch(`${API}/places`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, location })
    });
    document.getElementById("name").value = "";
    document.getElementById("location").value = "";
    getPlaces();
  } catch (err) {
    console.error("Fetch POST error:", err);
  }
}

document.getElementById("addBtn").addEventListener("click", addPlace);

getPlaces();