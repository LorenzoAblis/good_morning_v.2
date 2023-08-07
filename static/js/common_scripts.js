document.addEventListener('DOMContentLoaded', () => {
    function updateTime() {
        const currentTimeElement = document.getElementById('current-time');
        const now = new Date();
        let hours = now.getHours();
        const minutes = now.getMinutes().toString().padStart(2, '0');
        const meridiem = hours >= 12 ? 'PM' : 'AM';
    
        hours = hours % 12 || 12;
    
        const currentTimeString = `${hours}:${minutes} ${meridiem}`;
        currentTimeElement.textContent = currentTimeString;
    }
    
    updateTime();
    setInterval(updateTime, 1000);
});