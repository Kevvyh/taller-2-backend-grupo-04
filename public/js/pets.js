// @ts-check
// @ts-expect-error - Módulo servido vía CDN; TS no puede resolver la URL.
import Alpine from "https://cdn.jsdelivr.net/npm/alpinejs@3.14.8/dist/module.esm.js"
import { api, normalizeErrors, toast } from "./api.js"

/** @typedef {import("./api.js").Student} Student */
/** @typedef {import("./api.js").Pet} Pet */
/** @typedef {import("./api.js").ApiPayload} ApiPayload */

function createApp() {
	return {
		studentId: new URLSearchParams(window.location.search).get("studentId") || "",
		student: null,
		studentError: false,

		pets: [],
		loading: false,

		modal: { open: false, mode: "create", busy: false },
		form: { id: null, name: "", species: "", age: "" },
		errors: {},

		deleteModal: { open: false, pet: null, busy: false },

		async init() {
			if (!this.studentId) {
				this.studentError = true
				return
			}

			await this.loadStudent()

			if (this.student) {
				await this.loadPets()
			}
		},

		async loadStudent() {
			try {
				const data = /** @type {Student} */ (await api(`/students/${this.studentId}`))
				this.student = data
			} catch {
				this.studentError = true
			}
		},

		async loadPets() {
			this.loading = true

			try {
				const list = /** @type {{ items: Pet[] }} */ (
					await api(`/students/${this.studentId}/pets`)
				)
				this.pets = list.items
			} catch (err) {
				const message = (err && err.error) || "No se pudieron cargar las mascotas"
				toast(message)
			} finally {
				this.loading = false
			}
		},

		openCreate() {
			this.form = { id: null, name: "", species: "", age: "" }
			this.errors = {}
			this.modal = { open: true, mode: "create", busy: false }
		},

		openEdit(pet) {
			this.form = {
				id: pet.id,
				name: pet.name,
				species: pet.species,
				age: pet.age === undefined ? "" : String(pet.age),
			}
			this.errors = {}
			this.modal = { open: true, mode: "edit", busy: false }
		},

		closeModal() {
			this.modal.open = false
			this.errors = {}
		},

		async submit() {
			this.modal.busy = true
			this.errors = {}

			const id = this.form.id
			const method = id ? "PATCH" : "POST"
			const path = id ? `/students/${this.studentId}/pets/${id}` : `/students/${this.studentId}/pets`

			/** @type {{ name: string, species: string, age?: number }} */
			const body = {
				name: this.form.name,
				species: this.form.species,
			}

			if (this.form.age !== "") {
				body.age = Number(this.form.age)
			}

			try {
				await api(path, { method, body: JSON.stringify(body) })
				this.closeModal()
				toast(id ? "Mascota actualizada" : "Mascota creada", "success")
				await this.loadPets()
			} catch (error) {
				const err = /** @type {ApiPayload} */ (error)

				if (err?.errors) {
					this.errors = normalizeErrors(err.errors)
				} else {
					toast(err?.message ?? err?.error ?? "Ocurrió un error inesperado")
				}
			} finally {
				this.modal.busy = false
			}
		},

		openDelete(pet) {
			this.deleteModal = { open: true, pet, busy: false }
		},

		closeDelete() {
			this.deleteModal.open = false
		},

		async confirmDelete() {
			const pet = this.deleteModal.pet
			if (!pet) return

			this.deleteModal.busy = true

			try {
				await api(`/students/${this.studentId}/pets/${pet.id}`, { method: "DELETE" })
				this.closeDelete()
				toast("Mascota eliminada", "success")
				await this.loadPets()
			} catch (error) {
				const err = /** @type {ApiPayload} */ (error)
				toast(err?.error ?? "No se pudo eliminar la mascota")
			} finally {
				this.deleteModal.busy = false
			}
		},
	}
}

Alpine.data("app", createApp)
Alpine.start()