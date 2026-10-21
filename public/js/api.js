// @ts-check
// @ts-expect-error - Módulo servido vía CDN; TS no puede resolver la URL.
import { toast as sonnerToast } from "https://cdn.jsdelivr.net/npm/vanilla-sonner@0.5.2/dist/vanilla-sonner.es.min.mjs"

/**
 * @typedef {{ message: string }} FieldError
 * @typedef {Record<string, FieldError>} ValidationErrors
 * @typedef {{
 *   code?: number,
 *   success?: boolean,
 *   message?: string,
 *   timestamp?: string,
 *   data?: unknown,
 *   error?: string,
 *   errors?: ValidationErrors,
 * }} ApiPayload
 * @typedef {{
 *   id: string,
 *   name: string,
 *   username: string,
 *   email: string,
 *   age: number,
 *   createdAt: string,
 *   updatedAt: string,
 * }} Student
 * @typedef {{
 *   id: string,
 *   studentId: string,
 *   name: string,
 *   species: string,
 *   age?: number,
 *   createdAt: string,
 *   updatedAt: string,
 * }} Pet
 */

const API_BASE = "/api"

/**
 * Petición a la API. Devuelve `data` en caso de éxito o lanza el payload
 * estandarizado (`ApiPayload`) cuando el servidor responde con error.
 *
 * @template T
 * @param {string} path Ruta relativa al prefijo `/api`.
 * @param {RequestInit} [options] Opciones de `fetch`.
 * @returns {Promise<T>}
 */
async function api(path, options = {}) {
	const response = await fetch(`${API_BASE}${path}`, {
		headers: { "Content-Type": "application/json" },
		...options,
	})

	/** @type {ApiPayload} */
	const payload = await response.json()

	if (!response.ok) {
		throw payload
	}

	return /** @type {T} */ (payload.data)
}

/**
 * Normaliza `ValidationErrors` del servidor (`{ campo: { message } }`)
 * a un mapa `campo -> mensaje` para renderizar bajo cada input.
 *
 * @param {ValidationErrors} errors
 * @returns {Record<string, string>}
 */
function normalizeErrors(errors) {
	/** @type {Record<string, string>} */
	const result = {}

	for (const [field, entry] of Object.entries(errors)) {
		result[field] = entry.message
	}

	return result
}

/**
 * Muestra una notificación transitoria usando `vanilla-sonner`.
 *
 * @param {string} message Mensaje a mostrar.
 * @param {"success" | "error"} [type] Tipo de notificación.
 */
function toast(message, type = "error") {
	if (type === "success") sonnerToast.success(message)
	else sonnerToast.error(message)
}

export { api, normalizeErrors, toast }
