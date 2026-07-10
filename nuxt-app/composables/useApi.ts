interface HealthResponse {
  status: string
}

interface UploadResponse {
  id: string
  url: string
  type: string
  size: number
}

interface FileMetadata {
  id: string
  url: string
  type: string
  size: number
  createdAt?: string
}

class ApiError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number = 500,
    public readonly data: unknown = null,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export function useApi() {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBase as string

  async function health(): Promise<HealthResponse> {
    return request<HealthResponse>(`${baseUrl}/health`)
  }

  async function upload(file: File, type: string): Promise<UploadResponse> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('type', type)

    return request<UploadResponse>(`${baseUrl}/upload`, {
      method: 'POST',
      body: formData,
    })
  }

  async function getFile(id: string): Promise<FileMetadata> {
    return request<FileMetadata>(
      `${baseUrl}/files/${encodeURIComponent(id)}`,
    )
  }

  async function request<T>(
    url: string,
    options?: Parameters<typeof $fetch>[1],
  ): Promise<T> {
    try {
      return await $fetch<T>(url, options)
    } catch (error) {
      const fetchError = error as {
        statusCode?: number
        statusMessage?: string
        data?: { error?: string; message?: string }
        message?: string
      }

      const statusCode = fetchError.statusCode ?? 500
      const backendMessage =
        fetchError.data?.error ?? fetchError.data?.message ?? fetchError.statusMessage
      const message = backendMessage ?? fetchError.message ?? 'Request failed'

      throw new ApiError(message, statusCode, fetchError.data ?? null)
    }
  }

  return {
    health,
    upload,
    getFile,
  }
}

export { ApiError }
