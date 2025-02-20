/*********************************************************************************
 * 
 * Express server to serve Wordle.
 *
 * This server handles both Part 1 and Part2:
 * 
 * - For Part 1, simply put any static files (html, css, etc.) in the directory
 *   named "public".
 * 
 * - For Part 2, put the .ejs file in the directory named "views". Use the name
 *   of the file _without_ the .ejs extension as the route. For example, entering
 *   "wordle_part2" in the navigation bar will tell the server to render 
 *   "views/wordle_part2.ejs"
 * 
 *   Put any parameters for the template in paramsForPt2.
 * 
 ******************************************************************************/

// Parameters for Part 2.
// The purpose of allParamSets is so you can have several different test sets
// and easily switch between them.
const allParamSets = {
    set1: {
        maxAttempts: 5,
        guesses: ['stern', 'aroma', 'crook', 'frock']
    },
    set2: {
        maxAttempts: 8,
        guesses: ['audio', 'stern', 'glyph']
    }
}
const paramsForPt2 = allParamSets.set1;




/* Import the module containing ExpressJS */
const express = require('express')

/* Import other helpful modules */
const path = require('path')
const fs = require('fs')

/* Instantiate a server object*/
const app = express()
const port = 3000

/* Tell the server to use EJS by default */
app.set('view engine', 'ejs')

/* Set the views directory as the default location for 
   ejs template files */
app.set('views', path.join(__dirname, 'views'));

/* Serve any documents located in the public directory "as is"*/
app.use(express.static(path.join(__dirname, 'public')));

/* If the route/path begins with "wordle" (and is not the name of a file in public)
  then look for an .ejs file of the same name in the view directory. 
  ([^/]+ is a regular expression that matches one or more characters _except_ a slash.) */
app.get('/wordle:name([^/]+)', (req, res) => {
    const name = req.params.name;  // Extract the dynamic part after "wordle"

    /* Construct the EJS template name */
    const templateName = `wordle${name}`;
    
    /* Check if file exists. If it does, render the template.
       If not, send a 404 error */
    const ejsTemplateFileName = path.join(__dirname, 'views', `${templateName}.ejs`)
    if (fs.existsSync(ejsTemplateFileName)) {
        /* Render the EJS file */
        res.render(templateName, paramsForPt2, (err, html) => {
            if (err) {
                console.error('Error rendering EJS file:', err.message);
                // Handle error if the EJS file does not exist
                res.status(500).send('Problem rendering .ejs file: ', err.message);
            } else {
                res.send(html);
            }
        });
    } else {
        res.status(404).send(`Template file ${ejsTemplateFileName} not found.`)
    }
});

/* By default, serve public/wordle_part1.html. (Feel free to change this!) */
app.get('/', (_req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'wordle_part1.html'));
});
 
/* Launch the server */
app.listen(port, () => console.log(`Example app listening on port ${port}!`))