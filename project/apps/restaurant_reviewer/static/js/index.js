// This will be the object that will contain the Vue attributes

//const { default: axios } = require("axios");
// and be used to initialize it.
let app = {};
let MAX_RETURNED_RESTAURANTS = 20;

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

  // This is the Vue data.
  app.data = {
    currentUser: null,
    users: [],
    restaurants: [],
    text: "",
    results: [],
    followedUsers : []
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
    console.log("something");
    console.log(`in filterRestaurantadsfasdf ${app.vue.results}`);
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

  app.addRestaurant = function(restaurant) {

  }

  app.removeRestaurant = function(restaurant) {
    
  }

  // app.setFollow = function(user) {
  //   console.log(`userFollowed = ${user.username}`);
  //   fetch(follow_url, {
  //       method: "POST",
  //       headers: {
  //       "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({
  //       username: user.username,
  //       }),
  //   }).then((response) => response.json())
  //     .then((data) => {
  //     if (data.success) {
  //         user.isFollowing = !user.isFollowing;
  //         localStorage.setItem(user.id, user.isFollowing);
  //     }//end if
  //   });
  //   app.getUsers();

  // }
  app.setFollow = function(restaurant) {
    if(app.isFollowing(restaurant))
      app.removeRestaurant(restaurant);
    else
      app.addRestaurant(restaurant);
  }

  app.isFollowing = function (restaurant) {
    return restaurant.isFollowing;
  }

  app.addRestaurant = function(restaurant) {
    console.log(`userFollowed = ${restaurant.name}`);
    fetch(follow_url, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({
        username: restaurant.name,
        }),
    }).then((response) => response.json())
      .then((data) => {
      if (data.success) {
          restaurant.isFollowing = !restaurant.isFollowing;
          localStorage.setItem(restaurant.id, restaurant.isFollowing);
      }//end if
    });
    app.getRestaurants();

  }

  app.clearSearch = function() {
    app.vue.text = "";
    app.getRestaurants();
    app.vue.results = app.vue.results.slice(0, MAX_RETURNED_RESTAURANTS);
  }

  // This contains all the methods.
  app.methods = {
    filterRestaurants : app.filterRestaurants,
    getRestaurants : app.getRestaurants,
    addRestaurant : app.addRestaurant,
    removeRestaurant : app.removeRestaurant,
    setFollow : app.setFollow,
    clearSearch : app.clearSearch,
    isFollowing : app.isFollowing
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
    axios.get(get_current_user_url).then(function (responses) {
      app.vue.currentUser = responses.data.rows[0];
    });
  };

  // Call to the initializer.
  app.init();

  return app;
};

// This takes the (empty) app object, and initializes it,
// putting all the code in it.
init(app);
