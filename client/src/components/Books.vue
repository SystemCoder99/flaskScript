<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Books</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" @click="toggleAddBookModal">Add Book</button>
        <button type="button" class="btn btn-success btn-sm" @click="toggleSearchLocation">Search by Folder</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Location</th>
              <th scope="col">Title</th>
              <th scope="col">Tags</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.FolderPath }}</td>
              <td>{{ book.Title }}</td>
              <td>{{ book.tags }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm" @click="toggleEditBookModal(book)">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- search by location -->
    <!-- toggleSearchLocation -->
    <div
      ref="searchLocationModal"
      class="modal fade"
      :class="{ show: activeSearchLocationModal, 'd-block': activeSearchLocationModal }"
      tabindex="-1"
      role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Search By Folder Location</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleAddBookModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>

        </div>
      </div>
    </div>
    <!-- add new book modal -->
    <div
      ref="addBookModal"
      class="modal fade"
      :class="{ show: activeAddBookModal, 'd-block': activeAddBookModal }"
      tabindex="-1"
      role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add a new book</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleAddBookModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="addBookLoc" class="form-label">Location:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addBookLoc"
                  v-model="addBookForm.FolderPath"
                  placeholder="Enter location">
              </div>
              <div class="mb-3">
                <label for="addBookTitle" class="form-label">Title:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addBookTitle"
                  v-model="addBookForm.Title"
                  placeholder="Enter title">
              </div>
              <div class="mb-3">
                <label for="addBookTags" class="form-label">Tags:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addBookTitle"
                  v-model="addBookForm.tags"
                  placeholder="Enter tag">
              </div>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-primary btn-sm"
                  @click="handleAddSubmit">
                  Submit
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="handleAddReset">
                  Reset
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeAddBookModal" class="modal-backdrop fade show"></div>
    <!-- edit book modal -->
    <div
      ref="editBookModal"
      class="modal fade"
      :class="{ show: activeEditBookModal, 'd-block': activeEditBookModal }"
      tabindex="-1"
      role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Update</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleEditBookModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="editBookLocation" class="form-label">Location:</label>
                <input
                  type="text"
                  class="form-control"
                  id="editBookLocation"
                  v-model="editBookForm.FolderPath"
                  placeholder="Enter Location">
              </div>
              <div class="mb-3">
                <label for="editBookTitle" class="form-label">Title:</label>
                <input
                  type="text"
                  class="form-control"
                  id="editBookTitle"
                  v-model="editBookForm.Title"
                  placeholder="Enter Title">
              </div>
              <div class="mb-3">
                <label for="editBookTags" class="form-label">Tags:</label>
                <input
                  type="text"
                  class="form-control"
                  id="editBookTags"
                  v-model="editBookForm.tags"
                  placeholder="Enter Tags">
              </div>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-primary btn-sm"
                  @click="handleEditSubmit">
                  Submit
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="handleEditCancel">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeEditBookModal" class="modal-backdrop fade show"></div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      activeAddBookModal: false,
      addBookForm: {
        FolderPath: '',
        Title: '',
        tags: [],
      },
      activeEditBookModal: false,
      editBookForm: {
        id: '',
        FolderPath: '',
        Title: '',
        tags: '',
      },
      books:[],
    };
  },
  methods: {
    addBook(payload) {
      const path = 'http://localhost:5001/books';
      axios.post(path, payload)
        .then(() => {
          this.getBooks();
        })
        .catch((error) => {

          console.log(error);
          this.getBooks();
        });
    },
    getBooks() {
      const path = 'http://localhost:5001/books';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    handleAddReset() {
      this.initForm();
    },
    handleAddSubmit() {
      this.toggleAddBookModal();
      //let read = false;
      //if (this.addBookForm.read[0]) {
      //  read = true;
      //}
      const payload = {
        FolderPath: this.addBookForm.FolderPath,
        Title: this.addBookForm.Title,
        tags: this.addBookForm.tags, // property shorthand
      };
      this.addBook(payload);
      this.initForm();
    },
    initForm() {
      this.addBookForm.FolderPath = '';
      this.addBookForm.title = '';
      this.addBookForm.tags = [];
      this.editBookForm.id = '';
      this.editBookForm.FolderPath = '';
      this.editBookForm.Title = '';
      this.editBookForm.tags = '';
    },
    toggleAddBookModal() {
      const body = document.querySelector('body');
      this.activeAddBookModal = !this.activeAddBookModal;
      if (this.activeAddBookModal) {
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
      }
    },
    toggleEditBookModal(book) {
      if (book) {
        this.editBookForm = book;
      }
      const body = document.querySelector('body');
      this.activeEditBookModal = !this.activeEditBookModal;
      if (this.activeEditBookModal) {
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
      }
    },
    handleEditSubmit() {
      this.toggleEditBookModal(null);
      const payload = {
        FolderPath: this.editBookForm.FolderPath,
        Title: this.editBookForm.Title,
        tags: this.editBookForm.tags,
      };
      this.updateBook(payload, this.editBookForm.id);
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:5001/books/${bookID}`;
      axios.put(path, payload)
          .then(() => {
            this.getBooks();
          })
          .catch((error) => {
            console.error(error);
            this.getBooks();
          });
    },
    handleEditCancel() {
      this.toggleEditBookModal(null);
      this.initForm();
      this.getBooks();
    },
  },
  created() {
    this.getBooks();
  },
};
</script>