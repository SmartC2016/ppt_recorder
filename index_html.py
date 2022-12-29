index_html = """
<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>--TITLE-BROWSER--</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Display&display=swap');

            :root {
                /* https://www.color-hex.com/color-palette/184 */
                --background-gray: #999999;
                --medium-gray: #777777;
                --darker-gray: #333333;
                --font-gray: #111111;
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                font-family: 'Noto Sans Display', sans-serif;
                display: grid;
                margin: 5px;
                height: 100vh;
                background-color: var(--background-gray);
                grid-template-columns: 1fr;
                grid-template-rows: 0.02fr 0.02fr auto 0.05fr;
                /* if no description exists, then the grid-template area and rows could be changed ?! */
                grid-template-areas:
                    'title'
                    'description'
                    'main'
                    'footer';
                justify-content: center;
                gap: 5px;
                overflow: hidden;
            }

            .title {
                grid-area: title;
                display: flex;
                justify-content: center;
            }

            .description {
                grid-area: description;
                padding-bottom: 5px;
            }

            #main {
                grid-area: main;
                display: flex;
                justify-content: center;
                /* background-image: url("/img/221223_233115_test123.jpg"); */
                background-repeat: no-repeat;
                background-size: contain;
                background-position: center;
            }

            footer {
                grid-area: footer;
                display: flex;
                justify-content: center;
                margin: 10px;
                padding-bottom: 10px;
            }

            footer button {
                margin-left: 10px;
                margin-right: 10px;
                padding: 5px 10px;
                border-radius: 5px;
                background-color: var(--medium-gray);
                color: var(--font-gray);
                font-weight: bold;
                box-shadow: 5px 5px 20px 5px rgba(0, 0, 0, 0.7);
            }

            footer button:disabled {
                color: var(--background-gray);
            }

            footer button:hover:enabled {
                cursor: pointer;
            }
        </style>
    </head>

    <body>
        <section class="title">
            <!-- The title needs to be replaced -->
            <h1 class="title-headline">--TITLE--</h1>
        </section>
        <section class="description">
            <!-- the description needs to be replaced -->
            <p class="description-text">--DESCRIPTION--</p>
        </section>
        <section id="main">
            <!-- Here are the different images -->
        </section>
        <footer>
            <button id="button-backward">&lt;</button>
            <button id="button-forward">&gt;</button>
        </footer>
    </body>
    <script>
        let position = 0;
        // the list of pictures need to be replaced
        // const list_of_pics = ['221223_233119_test123.jpg', '221224_001407_test123.jpg', '221224_001419_test123.jpg', '4.jpg', '5.jpg', '6.jpg']
        const list_of_pics = --LIST_OF_PICS--;
        const numOfPictures = Object.keys(list_of_pics).length;
        const sectionMain = document.getElementById('main');
        const buttonForward = document.getElementById('button-forward');
        const buttonBack = document.getElementById('button-backward');

        buttonForward.addEventListener("click", nextPic);
        buttonBack.addEventListener("click", prevPic);

        checkBackButton();
        checkListLength();
        firstPic(); // only called once to set the initial (first) picture

        function checkListLength() {
            if (list_of_pics.length == 1) {
                buttonBack.disabled = true;
                buttonForward.disabled = true;
            }
        }

        function firstPic() {
            let newPic = `url(img/${list_of_pics[position]})`;
            sectionMain.style.backgroundImage = newPic;

        }

        function nextPic() {
            if (position < numOfPictures - 1) {
                position++;
                let newPic = `url(img/${list_of_pics[position]})`;
                sectionMain.style.backgroundImage = newPic;
                checkBackButton();
            }
            if (position == numOfPictures - 1) {
                buttonForward.disabled = true;
            }
        };

        function prevPic() {
            if (position > 0) {
                position--;
                let newPic = `url(img/${list_of_pics[position]})`;
                sectionMain.style.backgroundImage = newPic;
                checkBackButton();
            }
            if (position < numOfPictures - 1) {
                buttonForward.disabled = false;
            }
        }

        function checkBackButton() {
            if (position == 0) {
                buttonBack.disabled = true;
            } else {
                buttonBack.disabled = false;
            }
        };
    </script>

</html>
"""
