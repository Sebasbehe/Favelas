const API = "http://127.0.0.1:8000";
console.log("JS OK");

// ======================
// 🔐 LOGIN - ENVIAR OTP
// ======================
async function enviarOTP() {
    const email = document.getElementById("email")?.value.trim();
    const btn = document.getElementById("btnSend");

    if (!email) {
        alert("Ingresa un correo");
        return;
    }

    if (btn) {
        btn.disabled = true;
        btn.innerText = "Enviando...";
    }

    try {
        const res = await fetch(`${API}/auth/send-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.detail || "Error enviando OTP");
            return;
        }

        localStorage.setItem("email", email);
        window.location.href = "otp.html";

    } catch (err) {
        alert("Error de conexión con el servidor");
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerText = "Enviar código";
        }
    }
}

// ======================
// 🔐 OTP - VERIFICAR
// ======================
async function verificarOTP() {
    const email = localStorage.getItem("email");
    const otp = document.getElementById("otp")?.value.trim();
    const btn = document.getElementById("btnVerify");

    if (!otp) {
        alert("Ingresa el código OTP");
        return;
    }

    if (btn) {
        btn.disabled = true;
        btn.innerText = "Verificando...";
    }

    try {
        const res = await fetch(`${API}/auth/verify-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, otp })
        });

        const data = await res.json();

        if (!res.ok || !data.token) {
            alert(data.error || "OTP incorrecto");
            return;
        }

        localStorage.setItem("token", data.token);
        window.location.href = "dashboard.html";

    } catch (err) {
        alert("Error de conexión con el servidor");
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerText = "Verificar";
        }
    }
}

// ======================
// 🔒 PROTEGER DASHBOARD
// ======================
if (window.location.pathname.includes("dashboard.html")) {
    if (!localStorage.getItem("token")) {
        window.location.href = "login.html";
    }
}

// ======================
// 📚 DASHBOARD CRUD
// ======================
let estudianteEditando = null;

function getHeaders(isJSON = false) {
    const token = localStorage.getItem("token");

    const headers = {};

    if (token) {
        headers["token"] = token;
    }

    if (isJSON) {
        headers["Content-Type"] = "application/json";
    }

    return headers;
}

// ----------------------
async function cargarEstudiantes() {
    const res = await fetch(`${API}/students`, {
        headers: getHeaders()
    });

    if (res.status === 401) {
        alert("Sesión expirada");
        localStorage.clear();
        window.location.href = "login.html";
        return;
    }

    const data = await res.json();

    const lista = document.getElementById("lista");
    if (!lista) return;

    lista.innerHTML = "";

    data.forEach(e => {
        lista.innerHTML += `
            <li>
                ${e.nombre} - Edad: ${e.edad} - Nota: ${e.nota}
                <button onclick="editarEstudiante(${e.id}, ${JSON.stringify(e.nombre)}, ${e.edad}, ${e.nota})">✏️</button>
                <button onclick="eliminarEstudiante(${e.id})">🗑️</button>
            </li>
        `;
    });
}

// ----------------------
async function crearEstudiante() {
    const nombre = document.getElementById("nombre").value.trim();
    const edad = Number(document.getElementById("edad").value);
    const nota = Number(document.getElementById("nota").value);

    if (!nombre || isNaN(edad) || isNaN(nota)) {
        alert("Completa todos los campos");
        return;
    }

    await fetch(`${API}/students`, {
        method: "POST",
        headers: getHeaders(true),
        body: JSON.stringify({ nombre, edad, nota })
    });

    limpiarCampos();
    cargarEstudiantes();
}

// ----------------------
function editarEstudiante(id, nombre, edad, nota) {
    estudianteEditando = id;

    document.getElementById("nombre").value = nombre;
    document.getElementById("edad").value = edad;
    document.getElementById("nota").value = nota;

    document.getElementById("btnGuardar").style.display = "none";
    document.getElementById("btnActualizar").style.display = "inline";
}

// ----------------------
async function actualizarEstudiante() {
    await fetch(`${API}/students/${estudianteEditando}`, {
        method: "PUT",
        headers: getHeaders(true),
        body: JSON.stringify({
            nombre: document.getElementById("nombre").value.trim(),
            edad: Number(document.getElementById("edad").value),
            nota: Number(document.getElementById("nota").value)
        })
    });

    estudianteEditando = null;

    document.getElementById("btnGuardar").style.display = "inline";
    document.getElementById("btnActualizar").style.display = "none";

    limpiarCampos();
    cargarEstudiantes();
}

// ----------------------
async function eliminarEstudiante(id) {
    if (!confirm("¿Eliminar estudiante?")) return;

    await fetch(`${API}/students/${id}`, {
        method: "DELETE",
        headers: getHeaders()
    });

    cargarEstudiantes();
}

// ----------------------
function limpiarCampos() {
    document.getElementById("nombre").value = "";
    document.getElementById("edad").value = "";
    document.getElementById("nota").value = "";
}

// ----------------------
if (window.location.pathname.includes("dashboard.html")) {
    cargarEstudiantes();
}

// ----------------------
document.addEventListener("DOMContentLoaded", () => {
    const btnGuardar = document.getElementById("btnGuardar");
    const btnActualizar = document.getElementById("btnActualizar");

    if (btnGuardar) btnGuardar.addEventListener("click", crearEstudiante);
    if (btnActualizar) btnActualizar.addEventListener("click", actualizarEstudiante);
});