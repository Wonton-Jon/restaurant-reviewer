// This will be the object that will contain the Vue attributes

//const { default: axios } = require("axios");
// and be used to initialize it.
let app = {};
let MAX_RETURNED_USERS = 20;

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

  // This is the Vue data.
  app.data = {
    currentUser: null,
    users: [],
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

  app.filterUsers = function() {
    app.vue.results = app.vue.users.filter(function (item) {
      return (
        item.username.toLowerCase().indexOf(app.vue.text.toLowerCase()) >= 0
        && item.username.toLowerCase() != app.vue.currentUser.username.toLowerCase()
      );
    });
    app.vue.results = app.vue.results.slice(0, MAX_RETURNED_USERS);
  }

  app.getUsers = function () {
    axios.get(get_users_url).then(function (response) {
        app.vue.followedUsers = app.enumerate(response.data.followed);
        app.vue.users = response.data.followed.concat(response.data.unfollowed);
        app.vue.results = app.enumerate(app.vue.users).slice(0, MAX_RETURNED_USERS);
    });
}

  app.setFollow = function(user) {
    console.log(`userFollowed = ${user.username}`);
    fetch(follow_url, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({
        username: user.username,
        }),
    }).then((response) => response.json())
      .then((data) => {
      if (data.success) {
          user.isFollowing = !user.isFollowing;
          localStorage.setItem(user.id, user.isFollowing);
      }//end if
    });
    app.getUsers();

  }

  app.isFollowing = function (user) {
    return user.isFollowing;
  }

  app.clearSearch = function() {
    app.vue.text = "";
    app.getUsers();
    app.vue.results = app.vue.results.slice(0, MAX_RETURNED_USERS);
  }

  // This contains all the methods.
  app.methods = {
    filterUsers : app.filterUsers,
    getUsers : app.getUsers,
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
    app.getUsers();
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
