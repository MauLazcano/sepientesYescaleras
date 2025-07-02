function drawBoard(state) {
    let html = "<table>";
    for (let i = 9; i >= 0; i--) {
        html += "<tr>";
        for (let j = 0; j < 10; j++) {
            let cell = i % 2 === 0 ? i * 10 + j : i * 10 + (9 - j);
            html += `<td id="cell-${cell}">${cell}</td>`;
        }
        html += "</tr>";
    }
    html += "</table>";
    $('#board').html(html);

    // Mostrar jugadores
    state.players.forEach((p, i) => {
        let pos = state.positions[i];
        $(`#cell-${pos}`).append(`<img class="player-icon" src="/static/img/players/${p.icon}" title="${p.name}">`);
    });

    // Mostrar serpientes y escaleras
    for (let s in state.snakes) {
        $(`#cell-${s}`).append('<img src="/static/img/snake.png" class="player-icon">');
    }
    for (let l in state.ladders) {
        $(`#cell-${l}`).append('<img src="/static/img/ladder.png" class="player-icon">');
    }
}

function updateState() {
    $.get('/state', function(data) {
        drawBoard(data);
    });
}

function rollDice() {
    $.post('/roll', function(data) {
        if (data.error) {
            $('#result').text(data.error);
            return;
        }

        if (data.game_over) {
            showFinalResults(data.final_order);
            return;
        }

        $('#result').html(`${data.player} tiró ${data.dice[0]} + ${data.dice[1]} => va a ${data.position}`);

        if (data.winner) {
            showWinnerMessage(data.player);
        }

        updateState();
    });
}

function showWinnerMessage(playerName) {
    const winBanner = $('<div class="winner-banner">🎉 ¡' + playerName + ' ha llegado a la meta! 🎶</div>');
    $('body').append(winBanner);
    setTimeout(() => winBanner.fadeOut(1000, () => winBanner.remove()), 3000);
}

function showFinalResults(order) {
    let html = '<div class="final-banner"><h2>🏁 Juego Terminado</h2><table><tr><th>Lugar</th><th>Jugador</th></tr>';
    order.forEach((name, index) => {
        html += `<tr><td>${index + 1}</td><td>${name}</td></tr>`;
    });
    html += '</table></div>';
    $('body').append(html);
}


setInterval(updateState, 500);
