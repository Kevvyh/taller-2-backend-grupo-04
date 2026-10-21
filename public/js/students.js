// @ts-check
// @ts-expect-error - Módulo servido vía CDN; TS no puede resolver la URL.
import Alpine from "https://cdn.jsdelivr.net/npm/alpinejs@3.14.8/dist/module.esm.js"
import { api, normalizeErrors, toast } from "./api.js"

/** @typedef {import("./api.js").Student} Student */
/** @typedef {import("./api.js").ApiPayload} ApiPayload */

/**
 * @param {ApiPayload} err Payload de error estandarizado lanzado por `api`.
 */
function handleSubmitError(err) {
	if (err?.errors) {
		return normalizeErrors(err.errors)
	}

	return err?.message ?? err?.error ?? "Ocurrió un error inesperado"
}

function createApp() {
	return {
		students: [],
		loading: false,

		modal: { open: false, mode: "create", busy: false },
		form: { id: null, name: "", username: "", email: "", age: "" },
		errors: {},

		deleteModal: { open: false, student: null, busy: false },

		async init() {
			await this.load()
		},

		async load() {
			this.loading = true

			try {
				const list = /** @type {{ items: Student[] }} */ (await api("/students"))
				this.students = list.items
			} catch (err) {
				const message =
					(err && err.error) || "No se pudieron cargar los estudiantes"
				toast(message)
			} finally {
				this.loading = false
			}
		},

		openCreate() {
			this.form = { id: null, name: "", username: "", email: "", age: "" }
			this.errors = {}
			this.modal = { open: true, mode: "create", busy: false }
		},

		openEdit(student) {
			this.form = {
				id: student.id,
				name: student.name,
				username: student.username,
				email: student.email,
				age: String(student.age),
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
			const path = id ? `/students/${id}` : "/students"

			/** @type {{ name: string, username: string, email: string, age?: number }} */
			const body = {
				name: this.form.name,
				username: this.form.username,
				email: this.form.email,
			}

			if (this.form.age !== "") {
				body.age = Number(this.form.age)
			}

			try {
				await api(path, { method, body: JSON.stringify(body) })
				this.closeModal()
				toast(
					id ? "Estudiante actualizado" : "Estudiante creado",
					"success",
				)
				await this.load()
			} catch (error) {
				const result = handleSubmitError(/** @type {ApiPayload} */ (error))
				if (typeof result === "string") {
					toast(result)
				} else {
					this.errors = result
				}
			} finally {
				this.modal.busy = false
			}
		},

		openDelete(student) {
			this.deleteModal = { open: true, student, busy: false }
		},

		closeDelete() {
			this.deleteModal.open = false
		},

		async confirmDelete() {
			const student = this.deleteModal.student
			if (!student) return

			this.deleteModal.busy = true

			try {
				await api(`/students/${student.id}`, { method: "DELETE" })
				this.closeDelete()
				toast("Estudiante eliminado", "success")
				await this.load()
			} catch (error) {
				const err = /** @type {ApiPayload} */ (error)
				toast(err?.error ?? "No se pudo eliminar el estudiante")
			} finally {
				this.deleteModal.busy = false
			}
		},
	}
}

Alpine.data("app", createApp)
Alpine.start()