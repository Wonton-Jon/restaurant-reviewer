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
        console.log(`In getRestaurants: ${app.vue.restaurants}`);
        app.vue.results = app.enumerate(app.vue.restaurants).slice(0, MAX_RETURNED_RESTAURANTS);
    });
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
  //         user.isFollowed = !user.isFollowed;
  //         localStorage.setItem(user.id, user.isFollowed);
  //     }//end if
  //   });
  //   app.getUsers();

  // }
  app.setFollow = function(restaurant) {
    console.log(`in setFollow(): ${app.isFollowed(restaurant)}`);
    restaurant.isFollowed = !restaurant.isFollowed;
  }

  app.isFollowed = function (restaurant) {
    return restaurant.isFollowed;
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
    setFollow : app.setFollow,
    clearSearch : app.clearSearch,
    isFollowed : app.isFollowed
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
