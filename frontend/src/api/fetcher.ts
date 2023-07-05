import { type ApiSurface, type CrossSpeciesSimilarityResponse, type NiMareResponse } from '../types/surfaces'

const API_URL: string = process.env.REACT_APP_API_URL ?? 'http://localhost:8000'

const Endpoints = {
  getHemispheres: `${API_URL}/surfaces/hemispheres`,
  getCrossSpeciesSimilarity: `${API_URL}/features/cross_species`,
  getNimareTerms: `${API_URL}/features/nimare`
}

/**
 * Fetches the surface data for all surfaces.
 * @param species The species to fetch surfaces for.
 * @param side The side to fetch surfaces for.
 * @returns A Promise that resolves to an ApiSurfaceResponse object.
 */
export async function getSurfaces (species: string, side: string): Promise<ApiSurface> {
  const response = await fetch(`${Endpoints.getHemispheres}?species=${species}&side=${side}`)
  return await response.json()
}

/**
 * Fetches the similarity data for a given vertex on a surface.
 *
 * @param species - The species of the surface.
 * @param side - The side of the surface.
 * @param vertex - The vertex index on the surface.
 * @returns A Promise that resolves to a SimilarityResponse object.
 */
export async function getCrossSpeciesSimilarity (
  species: string,
  side: string,
  vertex: number
): Promise<CrossSpeciesSimilarityResponse> {
  const response = await fetch(
    `${Endpoints.getCrossSpeciesSimilarity}?seed_species=${species}&seed_side=${side}&seed_vertex=${vertex}`
  )
  return await response.json()
}

/**
 * Fetches the NiMare terms for a given vertex on a surface.
 *
 * @param surface - The API surface object.
 * @param vertex - The vertex index on the surface.
 * @returns A Promise that resolves to a SimilarityResponse object.
 */
export async function getNimareTerms (
  surface: ApiSurface,
  vertex: number
): Promise<NiMareResponse> {
  const coordinates = {
    x: surface.xCoordinate[vertex],
    y: surface.yCoordinate[vertex],
    z: surface.zCoordinate[vertex]
  }
  const response = await fetch(
    `${Endpoints.getNimareTerms}?x=${coordinates.x}&y=${coordinates.y}&z=${coordinates.z}`
  )
  return await response.json()
}