    <h2> choose a location </h2>

    <form method = 'post' action='/manage'>
      {{!selectStr}}
      <input type='submit' value='Choose'>
    </form>
    ___________________________________________________________________________________________________________
    <h2> Add a new location </h2>

    <form method='post' action='/manage'>
        <div>Name <input type='text' name='name'></div>
        <div>Latitude <input type='text'name='latitude'></div>
        <div>Longitude <input type='text' name='longitude'></div>
        <input type='submit' value='Add new location'>
    </form>

    ___________________________________________________________________________________________________________
        <h2> Select maps to display </h2>

    <form method='post' action='/manage'>
        <label class="container">1st DEC 12:00AM
            <input type="checkbox" checked="checked">
            <span class="checkmark"></span>
        </label>
        <label class="container">2nd DEC 12:00AM
            <input type="checkbox" checked="checked">
            <span class="checkmark"></span>
        </label>
        <label class="container">2nd DEC 12:00AM
            <input type="checkbox" checked="checked">
            <span class="checkmark"></span>
        </label>
        <label class="container">2nd DEC 12:00AM
            <input type="checkbox" checked="checked">
            <span class="checkmark"></span>
        </label>
        <label class="container">2nd DEC 12:00AM
            <input type="checkbox" checked="checked">
            <span class="checkmark"></span>
        </label>

    </form>

    ___________________________________________________________________________________________________________
        <h2> Select Presentation </h2>

    <form method='post' action='/manage'>
        <form action="">
            <input type="radio" name="gender" value="male"> As Selected Above
            <input type="radio" name="gender" value="female"> Today
            <input type="radio" name="gender" value="other"> Tomorrow
            <input type="radio" name="gender" value="other"> Max temperature each day
    </form>

    ___________________________________________________________________________________________________________