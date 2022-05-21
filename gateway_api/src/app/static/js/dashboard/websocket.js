var socket;

document.addEventListener('DOMContentLoaded', function () {
    socket = io();

    socket.on('connect', function () {
        socket.emit('state', { data: 'Connected!' });
    });


    socket.on('lockdata', function (data) {
        let lock = locks.find(i => i.id == parseFloat(data.lock))
        if (lock.tm) clearTimeout(lock.tm);
        
        prioritized = lock.priorities.includes(parseFloat(data.identifier));
        disabled = prioritized ? "disabled" : "";
        disabled_secondary = prioritized ? "": "disabled";

        text = prioritized ? "Prioritized" : "Prioritize";
        var contentString = `
            <div class="fs-6 mb-2"><b>${lock.name}</b> (${lock.id})</div>
            <div><b>Destination:</b> ${data.UNLocationCode} - ${data.facilityCode}</div>
            <div><b>Identifier:</b> ${data.identifier}</div>
            <div><b>Date Requested:</b> ${data.datetime_requested}</div>
            <div><b>Date Estimated:</b> ${data.datetime_estimated}</div>
            <div><b>Time Budget:</b> ${Math.round(data.time_budget / 60 / 60)}h</div>
            <div><b>Actual Time remaining:</b> ${Math.round(data.time_remaining / 60 / 60)}h</div>
            <div class="text-center mt-3">
                <button class="btn btn-sm btn-primary ${disabled}" onclick="function prioritize(e){locks.find(i => i.id == parseFloat(${data.lock})).priorities.push(${data.identifier}); e.classList.add('disabled'); e.innerText = 'Prioritized'};prioritize(this)">${text}
                </button>
                <button class="btn btn-sm btn-danger ${disabled_secondary}" onclick="function unprioritize(e){l=locks.find(i => i.id == parseFloat(${data.lock})); l.priorities.pop(l.priorities.findIndex(i=> i==parseFloat(${data.identifier}))); e.classList.add('disabled')};unprioritize(this)">Reset
                </button>
            </div>
        `;
        

        lock.infowindow.setContent(contentString);
        lock.infowindow.open({
            anchor: lock.marker,
            map: lock.map,
            shouldFocus: false
        });

        lock.tm = setTimeout(function () {
            lock.infowindow.close();
            lock.timeout = null;
            lock.priorities.pop(lock.priorities.findIndex(i=> i==parseFloat(data.identifier)));
        }, 2300);
    });





}, false);


