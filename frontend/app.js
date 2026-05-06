const API = "https://favelas-backend.onrender.com";

let estudianteEditando = null;

function getHeaders(isJSON = false) {
    const token = localStorage.getItem("token");

    const headers = {};

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    if (isJSON) {
        headers["Content-Type"] = "application/json";
    }

    return headers;
}

/* ================= OTP ================= */

async function enviarOTP() {
    const email = document.getElementById("email")?.value.trim();
    const btn = document.getElementById("btnSend");

    if (!email) return alert("Ingresa un correo");

    try {
        btn.disabled = true;
        btn.innerText = "Enviando...";

        const res = await fetch(`${API}/auth/send-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "Error enviando OTP");
        }

        if (data.otp) alert("Tu código OTP es: " + data.otp);

        localStorage.setItem("email", email);
        window.location.href = "otp.html";

    } catch (error) {
        alert(error.message);
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerText = "Enviar código";
        }
    }
}

async function verificarOTP() {
    const email = localStorage.getItem("email");
    const btn = document.getElementById("btnVerify");

    const digits = document.querySelectorAll(".otp-digit");
    const otp = [...digits].map(d => d.value).join("").trim();

    if (otp.length !== 6) return alert("Ingresa el OTP completo");

    try {
        btn.disabled = true;
        btn.innerText = "Verificando...";

        const res = await fetch(`${API}/auth/verify-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, otp })
        });

        const data = await res.json();

        if (!res.ok || !data.token) {
            throw new Error(data.detail || "OTP incorrecto");
        }

        localStorage.setItem("token", data.token);
        window.location.href = "dashboard.html";

    } catch (error) {
        alert(error.message);
    } finally {
        btn.disabled = false;
        btn.innerText = "Verificar código";
    }
}

/* ================= AUTH ================= */

if (window.location.pathname.includes("dashboard.html")) {
    if (!localStorage.getItem("token")) {
        window.location.href = "login.html";
    }
}

/* ================= CRUD STUDENTS ================= */

async function cargarEstudiantes() {
    try {
        const res = await fetch(`${API}/students`, {
            headers: getHeaders()
        });

        if (res.status === 401) {
            alert("Sesión expirada");
            logout();
            return;
        }

        const data = await res.json();
        const lista = document.getElementById("lista");

        if (!lista) return;

        lista.innerHTML = "";

        if (!data.length) {
            lista.innerHTML = `
                <tr>
                    <td colspan="5" style="text-align:center;padding:20px;">
                        No hay estudiantes registrados
                    </td>
                </tr>
            `;
            return;
        }

        data.forEach((e, i) => {
            lista.innerHTML += `
                <tr>
                    <td>${i + 1}</td>
                    <td>${e.nombre}</td>
                    <td>${e.edad}</td>
                    <td>${e.nota}</td>
                    <td>
                        <button onclick="editarEstudiante(${e.id}, '${encodeURIComponent(e.nombre)}', ${e.edad}, ${e.nota})">
                            ✏️
                        </button>
                        <button onclick="eliminarEstudiante(${e.id})">
                            🗑️
                        </button>
                    </td>
                </tr>
            `;
        });

    } catch (error) {
        console.error(error);
        alert("Error cargando estudiantes");
    }
}

async function crearEstudiante() {
    const nombre = document.getElementById("nombre").value.trim();
    const edad = Number(document.getElementById("edad").value);
    const nota = Number(document.getElementById("nota").value);

    if (!nombre || !edad || !nota) {
        return alert("Completa todos los campos");
    }

    try {
        const res = await fetch(`${API}/students`, {
            method: "POST",
            headers: getHeaders(true),
            body: JSON.stringify({ nombre, edad, nota })
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "No se pudo guardar");
        }

        limpiarCampos();
        cargarEstudiantes();

    } catch (error) {
        alert(error.message);
    }
}

function editarEstudiante(id, nombre, edad, nota) {
    estudianteEditando = id;

    document.getElementById("nombre").value = decodeURIComponent(nombre);
    document.getElementById("edad").value = edad;
    document.getElementById("nota").value = nota;

    document.getElementById("btnGuardar").style.display = "none";
    document.getElementById("btnActualizar").style.display = "inline-block";
    document.getElementById("btnCancelar").style.display = "inline-block";
}

async function actualizarEstudiante() {
    try {
        const res = await fetch(`${API}/students/${estudianteEditando}`, {
            method: "PUT",
            headers: getHeaders(true),
            body: JSON.stringify({
                nombre: document.getElementById("nombre").value.trim(),
                edad: Number(document.getElementById("edad").value),
                nota: Number(document.getElementById("nota").value)
            })
        });

        if (!res.ok) throw new Error("Error actualizando");

        cancelarEdicion();
        cargarEstudiantes();

    } catch (error) {
        alert(error.message);
    }
}

async function eliminarEstudiante(id) {
    if (!confirm("¿Eliminar estudiante?")) return;

    try {
        const res = await fetch(`${API}/students/${id}`, {
            method: "DELETE",
            headers: getHeaders()
        });

        if (!res.ok) throw new Error("Error eliminando");

        cargarEstudiantes();

    } catch (error) {
        alert(error.message);
    }
}

/* ================= HELPERS ================= */

function cancelarEdicion() {
    estudianteEditando = null;
    limpiarCampos();

    document.getElementById("btnGuardar").style.display = "inline-block";
    document.getElementById("btnActualizar").style.display = "none";
    document.getElementById("btnCancelar").style.display = "none";
}

function limpiarCampos() {
    document.getElementById("nombre").value = "";
    document.getElementById("edad").value = "";
    document.getElementById("nota").value = "";
}

function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}

/* ================= INIT ================= */

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("lista")) cargarEstudiantes();

    document.getElementById("btnGuardar")
        ?.addEventListener("click", crearEstudiante);

    document.getElementById("btnActualizar")
        ?.addEventListener("click", actualizarEstudiante);

    const digits = document.querySelectorAll(".otp-digit");
    digits.forEach((el, i) => {
        el.addEventListener("input", () => {
            if (el.value && i < digits.length - 1) digits[i + 1].focus();
        });

        el.addEventListener("keydown", e => {
            if (e.key === "Backspace" && !el.value && i > 0) {
                digits[i - 1].focus();
            }
        });
    });
});

window.logout = logout;
window.cancelarEdicion = cancelarEdicion;
window.editarEstudiante = editarEstudiante;
window.eliminarEstudiante = eliminarEstudiante;
