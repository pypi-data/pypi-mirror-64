// Entry point for the notebook bundle containing custom model definitions.

// debugger;
define(['base/js/namespace'], function(Jupyter) {
  'use strict';

  window['requirejs'].config({
    map: {
      '*': {
        jupyter_ascending: 'nbextensions/jupyter_ascending/index',
      },
    },
  });

  function get_notebook_name() {
    // return window.document.getElementById("notebook_name").innerHTML;
    return Jupyter.notebook.notebook_path;
  }

  function is_synced_notebook() {
    return get_notebook_name().includes('.synced.ipynb');
  }

  const target_name = 'AUTO_SYNC::notebook';

  function get_cell_from_notebook(cell_number) {
    let cell = Jupyter.notebook.get_cell(cell_number);

    while (cell === null) {
      // Kind of meh hack to just keep spamming cells at bottom until we get to the cell we want.
      Jupyter.notebook.insert_cell_at_bottom();

      cell = Jupyter.notebook.get_cell(cell_number);
    }

    return cell;
  }

  function update_cell_contents(data) {
    let cell = get_cell_from_notebook(data.cell_number);

    cell.set_text(data.cell_contents);
  }

  function execute_cell_contents(data) {
    let cell = get_cell_from_notebook(data.cell_number);

    cell.focus_cell();
    cell.execute();
  }

  function create_and_register_comm() {
    Jupyter.notebook.kernel.comm_manager.register_target(
      target_name,
      // comm is the frontend comm instance
      // msg is the comm_open message, which can carry data
      function(comm, _msg) {
        // Register handlers for later messages:
        comm.on_msg(function(msg) {
          console.log('Processing a message');
          console.log(msg);

          if (msg.content.data.command === 'update') {
            update_cell_contents(msg.content.data);
          } else if (msg.content.data.command === 'execute') {
            execute_cell_contents(msg.content.data);
          } else {
            // debugger;
            console.log('Got an unexpected message: ', msg);
          }
        });

        comm.on_close(function(msg) {
          console.log('close', msg);
        });
      }
    );
  }

  // Export the required load_ipython_extension function
  return {
    load_ipython_extension: function() {
      Jupyter.notebook.config.loaded
        .then(
          function on_config_loaded() {
            console.log('Loaded config...');
          },
          function on_config_error() {
            console.log('ERROR OF LOADING...???');
          }
        )
        .then(function actually_load() {
          console.log('===================================');
          // console.log(ascend);
          console.log('Loading Jupyter Ascending extension...');
          console.log('Opening... ', get_notebook_name());
          console.log('Is synced: ', is_synced_notebook());

          console.log('Attemping create comm...');
          if (Jupyter.notebook.kernel) {
            create_and_register_comm();
          } else {
            Jupyter.notebook.events.one('kernel_ready.Kernel', () => {
              create_and_register_comm();
            });
          }
          console.log('... success!');

          console.log('===================================');
        });
    },
  };
});
