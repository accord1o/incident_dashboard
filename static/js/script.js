document.addEventListener('DOMContentLoaded', function() {
    loadIncidents();

    // Настройка обработчиков фильтров
    document.getElementById('status-filter').addEventListener('change', loadIncidents);
    document.getElementById('category-filter').addEventListener('change', loadIncidents);
    document.getElementById('search-input').addEventListener('input', loadIncidents);
});

async function loadIncidents() {
    const status = document.getElementById('status-filter').value;
    const category = document.getElementById('category-filter').value;
    const search = document.getElementById('search-input').value;

    const response = await fetch(`/api/incidents?status=${status}&category=${category}&search=${search}`);
    const incidents = await response.json();

    renderIncidents(incidents);
}

function renderIncidents(incidents) {
    const container = document.getElementById('incidents-list');
    container.innerHTML = '';

    incidents.forEach(incident => {
        const incidentElement = createIncidentElement(incident);
        container.appendChild(incidentElement);
    });
}

function createIncidentElement(incident) {
    const element = document.createElement('div');
    element.className = 'incident-item';
    element.dataset.id = incident.id;

    // Определение цвета статуса
    let statusClass = 'status-new';
    let statusText = 'Новая';

    if (incident.status === 'confirmed') {
        statusClass = 'status-confirmed';
        statusText = 'Подтверждена';
    } else if (incident.status === 'closed') {
        statusClass = 'status-closed';
        statusText = 'Закрыта';
    } else if (incident.status === 'rejected') {
        statusClass = 'status-rejected';
        statusText = 'Отклонена';
    }

    element.innerHTML = `
        <div class="incident-header">
            <div class="incident-title">
                <i class="fas fa-exclamation-circle"></i>
                ${incident.problem_summary}
            </div>
            <div>
                <span class="incident-status ${statusClass}">${statusText}</span>
                <span class="incident-category">Категория ${incident.category}</span>
            </div>
        </div>

        <div class="incident-meta">
            <span><i class="far fa-clock"></i> ${incident.detection_time}</span>
            <span><i class="fas fa-microchip"></i> ${incident.affected_systems}</span>
            <span><i class="fas fa-user"></i> ${incident.responsible}</span>
        </div>

        <p>${incident.technical_details || ''}</p>

        <div class="incident-actions">
            ${incident.status === 'new' ? `
                <button class="btn btn-success btn-sm" onclick="openConfirmModal(${incident.id})">
                    <i class="fas fa-check-circle"></i> Подтвердить
                </button>
                <button class="btn btn-danger btn-sm" onclick="openRejectModal(${incident.id})">
                    <i class="fas fa-times-circle"></i> Отклонить
                </button>
            ` : ''}

            <button class="btn btn-outline btn-sm" onclick="openCategoryModal(${incident.id})">
                <i class="fas fa-tag"></i> Изменить категорию
            </button>

            ${!incident.war_room_url ? `
                <button class="btn btn-outline btn-sm" onclick="createWarRoom(${incident.id})">
                    <i class="fas fa-video"></i> Создать комнату
                </button>
            ` : `
                <a href="${incident.war_room_url}" target="_blank" class="btn btn-outline btn-sm">
                    <i class="fas fa-video"></i> Перейти в комнату
                </a>
            `}

            <button class="btn btn-outline btn-sm" onclick="notifyBusiness(${incident.id})">
                <i class="fas fa-bell"></i> Оповестить бизнес
            </button>

            ${incident.status !== 'closed' && incident.status !== 'rejected' ? `
                <button class="btn btn-primary btn-sm" onclick="openCloseModal(${incident.id})">
                    <i class="fas fa-lock"></i> Закрыть аварию
                </button>
            ` : ''}
        </div>
    `;

    return element;
}

// Функции для работы с модальными окнами
function openConfirmModal(incidentId) {
    const modalHtml = `
        <div class="modal active" id="confirm-modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3><i class="fas fa-check-circle"></i> Подтверждение аварии</h3>
                    <button class="close-modal" onclick="closeModal('confirm-modal')">&times;</button>
                </div>
                <div class="modal-body">
                    <p>Вы подтверждаете, что это реальная авария, требующая немедленного вмешательства?</p>
                    <div class="form-group">
                        <label for="confirm-comment">Комментарий (необязательно)</label>
                        <textarea id="confirm-comment" class="form-control" placeholder="Дополнительная информация..."></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-outline" onclick="closeModal('confirm-modal')">Отмена</button>
                    <button class="btn btn-success" onclick="confirmIncident(${incidentId})">Подтвердить аварию</button>
                </div>
            </div>
        </div>
    `;

    document.getElementById('modals-container').innerHTML = modalHtml;
}

async function confirmIncident(incidentId) {
    const comment = document.getElementById('confirm-comment').value;

    await fetch(`/api/incidents/${incidentId}/confirm`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ comment })
    });

    closeModal('confirm-modal');
    loadIncidents();
}

// Аналогичные функции для reject, changeCategory, closeIncident и createWarRoom

function closeModal(modalId) {
    document.getElementById(modalId).remove();
}

function refreshIncidents() {
    loadIncidents();
    alert('Данные обновлены');
}

function createIncidentElement(incident) {
    const element = document.createElement('div');
    element.className = 'incident-item';
    element.dataset.id = incident.id;

    // Определение цвета статуса
    let statusClass = 'status-new';
    let statusText = 'Новая';

    if (incident.status === 'confirmed') {
        statusClass = 'status-confirmed';
        statusText = 'Подтверждена';
    } else if (incident.status === 'closed') {
        statusClass = 'status-closed';
        statusText = 'Закрыта';
    } else if (incident.status === 'rejected') {
        statusClass = 'status-rejected';
        statusText = 'Отклонена';
    }

    // Форматирование даты
    const detectionTime = new Date(incident.detection_time);
    const formattedDate = `${detectionTime.getDate().toString().padStart(2, '0')}.${(detectionTime.getMonth() + 1).toString().padStart(2, '0')}.${detectionTime.getFullYear()} ${detectionTime.getHours().toString().padStart(2, '0')}:${detectionTime.getMinutes().toString().padStart(2, '0')}`;

    element.innerHTML = `
        <div class="incident-title">
            <span class="incident-status ${statusClass}">${statusText}</span>
            ${incident.problem_summary}
        </div>

        <div class="incident-meta">
            <span><i class="far fa-clock"></i> ${formattedDate}</span>
            <span><i class="fas fa-microchip"></i> ${incident.affected_systems}</span>
            <span><i class="fas fa-user"></i> ${incident.responsible}</span>
            ${incident.attachments ? `<span><i class="fas fa-file-pdf"></i> ${incident.attachments}</span>` : ''}
        </div>

        <div class="incident-desc">
            ${incident.technical_details || ''}
        </div>

        <div class="incident-actions">
            ${incident.status === 'new' ? `
                <button class="btn btn-success btn-sm" onclick="openConfirmModal(${incident.id})">
                    <i class="fas fa-check-circle"></i> Подтвердить
                </button>
                <button class="btn btn-danger btn-sm" onclick="openRejectModal(${incident.id})">
                    <i class="fas fa-times-circle"></i> Отклонить
                </button>
            ` : ''}

            <button class="btn btn-outline btn-sm" onclick="openCategoryModal(${incident.id})">
                <i class="fas fa-tag"></i> Изменить категорию
            </button>

            ${!incident.war_room_url ? `
                <button class="btn btn-outline btn-sm" onclick="createWarRoom(${incident.id})">
                    <i class="fas fa-video"></i> Создать комнату
                </button>
            ` : `
                <a href="${incident.war_room_url}" target="_blank" class="btn btn-outline btn-sm">
                    <i class="fas fa-video"></i> Перейти в комнату
                </a>
            `}

            <button class="btn btn-outline btn-sm" onclick="notifyBusiness(${incident.id})">
                <i class="fas fa-bell"></i> Оповестить бизнес
            </button>

            ${incident.status !== 'closed' && incident.status !== 'rejected' ? `
                <button class="btn btn-primary btn-sm" onclick="openCloseModal(${incident.id})">
                    <i class="fas fa-lock"></i> Закрыть аварию
                </button>
            ` : ''}
        </div>
    `;

    return element;
}

function createIncidentElement(incident) {
    const element = document.createElement('div');
    element.className = 'incident-item';
    element.textContent = incident.problem_summary;
    return element;
}