const poolTable = document.getElementById('pool');
let poolsData = {};
let mapsData = {};
let isSupporter = false;

// format drain time from seconds to MM:SS
function formatDrain(sec) {
    sec = Math.round(sec);
    const min = Math.floor(sec / 60);
    const s = sec % 60;
    return `${min}:${s.toString().padStart(2, '0')}`;
}
// get tournament from URL parameter
function getTournamentFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('tn');
}
// set tournament in URL
function setTournamentInUrl(tournament) {
    const params = new URLSearchParams(window.location.search);
    if (tournament) {params.set('tn', tournament)} else {params.delete('tn')}
    window.history.replaceState({}, '', `${window.location.pathname}?${params}`);
}

// load pools.json and maps.json on page load
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const poolsResponse = await fetch('/data/pools.json');
        poolsData = await poolsResponse.json();
        const mapsResponse = await fetch('/data/maps.json');
        mapsData = await mapsResponse.json();
        const mappoolCount = Object.values(poolsData).reduce((sum, t) => sum + Object.keys(t.mappools).length, 0);
        subtitle.textContent = `${Object.keys(poolsData).length} tournaments, ${mappoolCount} mappools, ${Object.keys(mapsData).length} maps`
        // populate tournament select
        Object.keys(poolsData).forEach(tournament => {
            const option = document.createElement('option');
            option.value = tournament;
            option.textContent = tournament;
            selectTournament.appendChild(option);
        });
        
        // populate mappool on tournament change
        selectTournament.addEventListener('change', () => {
            const selectedTournament = selectTournament.value;
            setTournamentInUrl(selectedTournament);
            selectMappool.innerHTML = '';
            poolTable.innerHTML = '';
            if (selectedTournament && poolsData[selectedTournament]) {
                // update forum link
                const forumLink = document.getElementById('forumLink');
                if (poolsData[selectedTournament].forum) {
                    forumLink.href = poolsData[selectedTournament].forum;
                    forumLink.style.display = 'inline';
                } else {
                    forumLink.style.display = 'none';
                }
                Object.keys(poolsData[selectedTournament].mappools).forEach(mappool => {
                    const option = document.createElement('option');
                    option.value = mappool;
                    option.textContent = mappool;
                    selectMappool.appendChild(option);
                });
                // trigger mappool change event to display the first pool
                selectMappool.dispatchEvent(new Event('change'));
            }
        });
        
        // populate table on mappool change
        selectMappool.addEventListener('change', () => {
            const selectedTournament = selectTournament.value;
            const selectedMappool = selectMappool.value;
            poolTable.innerHTML = '';
            
            if (selectedTournament && selectedMappool && poolsData[selectedTournament]) {
                const slots = poolsData[selectedTournament].mappools[selectedMappool];
                // create header row
                const headerRow = document.createElement('tr');
                const slotHeader = document.createElement('th');
                slotHeader.textContent = 'Slot';
                headerRow.appendChild(slotHeader);
                
                const dataHeaders = ['Map', 'Mapper', 'SR', 'OD', 'HP', 'BPM', 'Drain', 'Link'];
                dataHeaders.forEach(header => {
                    const th = document.createElement('th');
                    th.textContent = header;
                    headerRow.appendChild(th);
                });
                poolTable.appendChild(headerRow);
                
                // create data rows
                Object.entries(slots).forEach(([slot, mapId]) => {
                    const mapData = mapsData[mapId.toString()];
                    if (!mapData) return;
                    const row = document.createElement('tr');
                    // add color class based on slot type
                    const slotTypes = ['NM', 'HD', 'HR', 'DT', 'FM', 'HT', 'EZ', 'TB', 'EX'];
                    for (const slotType of slotTypes) {
                        if (slot.startsWith(slotType)) {
                            row.classList.add(slotType.toLowerCase());
                            break;
                        }
                    }
                    // slot column
                    const slotCell = document.createElement('td');
                    slotCell.innerHTML = `<b>${slot}</b>`;
                    row.appendChild(slotCell);
                    // map data columns
                    const hrMultiplier = slot.includes('HR') ? 1.4 : 1;
                    const dtMultiplier = slot.includes('DT') ? 1.5 : 1;
                    const dtArrow = slot.includes('DT') ? '⬆' : '';
                    const sr = Math.round(mapData.sr * 100) / 100;
                    const od = Math.round(mapData.od * hrMultiplier * 100) / 100;
                    const hp = Math.round(mapData.hp * hrMultiplier * 100) / 100;
                    const values = [
                        `${mapData.artist} - ${mapData.title} [${mapData.version}]`,
                        mapData.mapper,
                        `${sr}★${dtArrow}`,
                        `${od}${dtArrow}`,
                        `${hp}${dtArrow}`,
                        Math.round(mapData.bpm * dtMultiplier),
                        formatDrain(mapData.drain / dtMultiplier)
                    ];
                    values.forEach((value, index) => {
                        const td = document.createElement('td');
                        td.textContent = value;
                        // apply cover image as background for the Map cell (first column)
                        if (index === 0 && mapData.cover) {
                            td.style.backgroundImage = `linear-gradient(to right, rgba(0, 0, 0, 0.80), rgba(0, 0, 0, 0.40)), url('${mapData.cover}_2x')`;
                            td.style.backgroundSize = 'cover';
                            td.style.backgroundPosition = 'center';
                            td.style.color = '#fff';
                            td.style.textShadow = '2px 2px 4px rgba(0, 0, 0, 0.8)';
                        }
                        row.appendChild(td);
                    });
                    // add link column
                    const linkCell = document.createElement('td');
                    const linkUrl = isSupporter ? `osu://b/${mapId}` : `https://osu.ppy.sh/b/${mapId}`;
                    const linkElement = document.createElement('a');
                    linkElement.href = linkUrl;
                    linkElement.style.fontSize = '15px';
                    linkElement.textContent = '🔗';
                    linkElement.target = isSupporter ? '_self' : '_blank';
                    linkCell.appendChild(linkElement);
                    row.appendChild(linkCell);
                    
                    poolTable.appendChild(row);
                });
            }
        });
        
        // trigger initial mappool population
        if (Object.keys(poolsData).length > 0) {
            const tournamentFromUrl = getTournamentFromUrl();
            if (tournamentFromUrl && poolsData[tournamentFromUrl]) {
                selectTournament.value = tournamentFromUrl;
            }
            selectTournament.dispatchEvent(new Event('change'));
        }
        // handle supporter checkbox change
        supporterCheckbox.addEventListener('change', () => {
            isSupporter = supporterCheckbox.checked;
            selectMappool.dispatchEvent(new Event('change'));
        });
        // handle theme selection
        const themeRadios = document.querySelectorAll('input[name="theme"]');
        themeRadios.forEach(radio => {
            radio.addEventListener('change', (e) => {
                const theme = e.target.value;
                document.body.className = `theme-${theme}`;
                localStorage.setItem('selectedTheme', theme);
            });
        });
        // load saved theme or set default
        const savedTheme = localStorage.getItem('selectedTheme') || 'classic';
        document.body.className = `theme-${savedTheme}`;
        document.querySelector(`input[name="theme"][value="${savedTheme}"]`).checked = true;
    } catch (error) {
        console.error('Error loading JSON files:', error);
    }
});