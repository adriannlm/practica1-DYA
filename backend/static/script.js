// Gestión del token
function guardarToken(token) {
    localStorage.setItem('token', token);
}

function obtenerToken() {
    return localStorage.getItem('token');
}

function eliminarToken() {
    localStorage.removeItem('token');
}

// Gestión de la interfaz
function mostrarSeccion(seccionId) {
    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('registerSection').style.display = 'none';
    document.getElementById('mainContent').style.display = 'none';
    document.getElementById(seccionId).style.display = 'block';
}

// Eventos de navegación
document.getElementById('showRegister').addEventListener('click', (e) => {
    e.preventDefault();
    mostrarSeccion('registerSection');
});

document.getElementById('showLogin').addEventListener('click', (e) => {
    e.preventDefault();
    mostrarSeccion('loginSection');
});

document.getElementById('logoutBtn').addEventListener('click', () => {
    eliminarToken();
    mostrarSeccion('loginSection');
});

// Registro de médico
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = {
        nombre: document.getElementById('registerNombre').value,
        email: document.getElementById('registerEmail').value,
        password: document.getElementById('registerPassword').value,
        especialidad: document.getElementById('registerEspecialidad').value
    };

    try {
        const response = await fetch('/registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error('Error en el registro');
        }

        alert('Registro exitoso. Por favor, inicia sesión.');
        mostrarSeccion('loginSection');
    } catch (error) {
        console.error('Error:', error);
        alert('Error en el registro: ' + error.message);
    }
});

// Login
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new URLSearchParams();
    formData.append('username', document.getElementById('loginEmail').value);
    formData.append('password', document.getElementById('loginPassword').value);

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error('Credenciales inválidas');
        }

        const data = await response.json();
        guardarToken(data.access_token);
        mostrarSeccion('mainContent');
        cargarPacientes();
    } catch (error) {
        console.error('Error:', error);
        alert('Error en el inicio de sesión: ' + error.message);
    }
});

// Gestión de pacientes
async function cargarPacientes() {
    try {
        const response = await fetch('/pacientes/', {
            headers: {
                'Authorization': `Bearer ${obtenerToken()}`
            }
        });
        if (!response.ok) {
            throw new Error('Error al cargar los pacientes');
        }
        const pacientes = await response.json();
        mostrarPacientes(pacientes);
    } catch (error) {
        console.error('Error:', error);
        if (error.message.includes('401')) {
            mostrarSeccion('loginSection');
        }
    }
}

function mostrarPacientes(pacientes) {
    const listaPacientes = document.getElementById('listaPacientes');
    listaPacientes.innerHTML = '';

    pacientes.forEach(paciente => {
        const card = document.createElement('div');
        card.className = 'paciente-card';
        card.innerHTML = `
            <h3>${paciente.nombre}</h3>
            <p>Edad: ${paciente.edad} años</p>
            <p>Historial: ${paciente.historialMedico}</p>
            <button onclick="eliminarPaciente(${paciente.id})" class="btn btn-danger">Eliminar</button>
        `;
        listaPacientes.appendChild(card);
    });
}

document.getElementById('formularioPaciente').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = {
        nombre: document.getElementById('nombre').value,
        edad: parseInt(document.getElementById('edad').value),
        historialMedico: document.getElementById('historialMedico').value
    };

    try {
        const response = await fetch('/pacientes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${obtenerToken()}`
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error('Error al crear el paciente');
        }

        document.getElementById('formularioPaciente').reset();
        cargarPacientes();
    } catch (error) {
        console.error('Error:', error);
        if (error.message.includes('401')) {
            mostrarSeccion('loginSection');
        }
    }
});

async function eliminarPaciente(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar este paciente?')) {
        return;
    }

    try {
        const response = await fetch(`/pacientes/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${obtenerToken()}`
            }
        });

        if (!response.ok) {
            throw new Error('Error al eliminar el paciente');
        }

        cargarPacientes();
    } catch (error) {
        console.error('Error:', error);
        if (error.message.includes('401')) {
            mostrarSeccion('loginSection');
        }
    }
}

// Verificar autenticación al cargar la página
if (obtenerToken()) {
    mostrarSeccion('mainContent');
    cargarPacientes();
} else {
    mostrarSeccion('loginSection');
}