let city = "your-default-city"

let express = require(`express`);
let {PythonShell} = require('python-shell');
let app = express();
let port = 3001;

app.listen(port, function () {
    console.log(`http://localhost:${port}`);
})
app.use(express.static(`public`));
const hbs = require('hbs');
app.set('views', 'views');
app.set('view engine', 'hbs');
app.use(express.urlencoded({ extended: true }))

app.get('/', (req, res) => {
    if (req.query.city){
        city = req.query.city
    }
    let weather
    pyshell = new PythonShell('main.py');
    pyshell.send(city, { mode: 'json', pythonOptions: ['-u'] });
    pyshell.on('message', function (message) {
        weather = JSON.parse(message);
    pyshell.end(function (err) {
        if (err != undefined){res.render(`404`);}
        else{res.render(`index`,{weather: weather});}})})})