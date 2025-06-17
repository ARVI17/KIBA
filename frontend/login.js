const API = import.meta.env.VITE_API_URL;
console.info("Login a", `${API}/login`);

export async function login(email, password) {
  if (!email.trim() || !password) {
    alert("Completa ambos campos");
    return;
  }
  try {
    const res = await fetch(`${API}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correo: email, contrasena: password })
    });
    const data = await res.json();
    if (!res.ok) {
      console.error(data);
      alert("Error al iniciar sesión: " + data.error);
      return;
    }
    return data;
  } catch (err) {
    console.error(err);
    alert("Error de red: " + err.message);
  }
}
