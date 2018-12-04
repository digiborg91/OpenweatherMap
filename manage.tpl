    <h2> Select Locations to display </h2>

    <form>
        %for place in places:
            <input type="checkbox" name="checkboxes[]" value="{{place}}" checked/> {{place}}
            %end
            <input type='submit' value='Update Availability'>
    </form>
    ___________________________________________________________________________________________________________
    <h2> Add a new location </h2>

    <form method='post' action='/addPlace'>
        <div>Name <input type='text' name='name'></div>
        <div>Latitude <input type='text'name='latitude'></div>
        <div>Longitude <input type='text' name='longitude'></div>
        <input type='submit' value='Add new location'>

    </form>

    ___________________________________________________________________________________________________________
        <h2> Select maps to display </h2>

    <form>
        %for stamp in timestampData:
            <input type="checkbox" name="checkboxes[]" value="{{stamp}}" checked/> {{stamp}}
            %end
                        <input type='submit' value='update map'>
    </form>

    ___________________________________________________________________________________________________________
        <h2> Select Presentation </h2>

    <form method='post' action='/manage'>
        <form action="">
            <input type="radio" name="gender" value="male"> As Selected Above
            <input type="radio" name="gender" value="female"> Today
            <input type="radio" name="gender" value="other"> Tomorrow
            <input type="radio" name="gender" value="other"> Max temperature each day
            <input type='submit' value='Update presentation selection'>
    </form>

    ___________________________________________________________________________________________________________
    <br>
    <a href='/'>Show Map</a>
    </br>