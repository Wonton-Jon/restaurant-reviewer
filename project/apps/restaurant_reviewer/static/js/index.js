// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};
let MAX_RETURNED_RESTAURANTS = 20;

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

  // This is the Vue data.
  app.data = {
    users: [],
    restaurants: [],
    text: "",
    results: [],
    displayRestaurants : [],
    showAllRestaurants : true
  };

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  app.filterRestaurants = function() {
    if(app.vue.restaurants.length > 0){
      app.vue.results = app.vue.restaurants.filter(function (restaurant) {
      return (
        restaurant.name.toLowerCase().indexOf(app.vue.text.toLowerCase()) >= 0
      );
    });
  }//end if
    app.vue.results = app.vue.results.slice(0, MAX_RETURNED_RESTAURANTS);
  }

  app.getRestaurants = function () {
    axios.get(get_restaurants_url).then(function (response) {
        app.vue.restaurants = response.data.restaurants;
        app.vue.results = app.enumerate(app.vue.restaurants).slice(0, MAX_RETURNED_RESTAURANTS);
    });
  }

  app.setFollow = function(restaurant) {
    restaurant.isFollowed = !restaurant.isFollowed;
    axios.post(follow_url, {
      restaurant_id : restaurant.id,
      is_followed : restaurant.isFollowed
    });
  }

  app.isFollowed = function (restaurant) {
    return restaurant.isFollowed;
  }

  app.clearSearch = function() {
    app.vue.text = "";
    app.getRestaurants();
    app.vue.results = app.vue.results.slice(0, MAX_RETURNED_RESTAURANTS);
  }

  app.toggleDisplay = function(value) {
    console.log(`value: ${value}`)    
    console.log(`app.vue.showAllRestaurants: ${app.vue.showAllRestaurants}`)

    app.vue.showAllRestaurants = value;
    if(value) {
      app.vue.displayRestaurants = app.vue.restaurants;
    } else{
    //If set to show saved, then set display to show only followed restaurants
      app.vue.displayRestaurants = []
      for (var i = 0; i < app.vue.restaurants.length; i++) {
        if(app.vue.restaurants[i].isFollowed) {
          app.vue.displayRestaurants.unshift(app.vue.restaurants[i]);
          app.vue.displayRestaurants.sort((a, b) => (a.rating < b.rating) ? 1 : -1)
        }//end if
      }//end for
    }//end if
  }//end else


  app.setStars = (restaurant, num_stars) => {
    
    console.log("Hello from app.set_stars " + num_stars + restaurant);
    
    // Sets the stars on the server.
    axios.post(set_stars_url, {restaurant_id: restaurant.id, rating: num_stars}).then(() => {    app.getRestaurants();  app.vue.toggleDisplay(true);  });


};

  // This contains all the methods.
  app.methods = {
    filterRestaurants : app.filterRestaurants,
    getRestaurants : app.getRestaurants,
    setFollow : app.setFollow,
    clearSearch : app.clearSearch,
    isFollowed : app.isFollowed,
    toggleDisplay : app.toggleDisplay,
    setStars : app.setStars
  };

  // This creates the Vue instance.
  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    methods: app.methods,
  });

  // And this initializes it.
  app.init = () => {
    app.getRestaurants();

  };

  // Call to the initializer.
  app.init();

  return app;
};

// This takes the (empty) app object, and initializes it,
// putting all the code in it.
init(app);