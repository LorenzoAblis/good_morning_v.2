document.addEventListener('DOMContentLoaded', () => {
    function getDay() {
        const currentDayElement = document.getElementById('current-day');
        const now = new Date();
        const dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        
        const month = monthNames[now.getMonth()];
        const day = dayNames[now.getDay()];
        const dateNumber = now.getDate();
    
        const currentDayString = `${day}, ${month} ${dateNumber}`;
        currentDayElement.textContent = currentDayString;
    }
    
    getDay();
});