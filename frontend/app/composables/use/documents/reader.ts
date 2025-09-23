import { parse } from 'papaparse'
import type { ParseResult } from 'papaparse'
import type { Refeable, Nullable, Undefineable } from '~/types'

type _File = Undefineable<File>

type SingleRow<T> = Record<keyof T, string | number | null>

interface ProcessedCsv<F> {
  headers: (keyof F)[]
  data: SingleRow<F>[],
  meta: {
    totalRows: number
    totalColumns: number
    delimiter: string,
    linebreak: string
    aborted: false,
    truncated: false
  }
}

type AllowedTypes = 'application/json' | 'text/csv' | 'application/csv' | 'text/plain'

type FileExtension = 'json' | 'csv' | 'txt' | (string & {})

/**
 * Composable used for reading a csv or json file
 * being uploaded by the user
 */
export function useFileReader<T = { name: string }>() {
  const file = ref<_File>()

  const MAX_FILE_SIZE = 10 * 1024 * 1024

  const ALLOWED_TYPES: Record<AllowedTypes, 'json' | 'csv'> = {
    'application/json': 'json',
    'text/csv': 'csv',
    'application/csv': 'csv',
    'text/plain': 'csv' // Sometimes CSV files are detected as plain text
  }

  const isValid = computed(() => {
    if (isDefined(file)) {
      // Check file size
      if (file.value.size > MAX_FILE_SIZE) {
        throw new Error('File size exceeds 10MB limit')
      }
  
      // Check file extension as fallback
      const extension = file.value.name.toLowerCase().split('.').pop() as FileExtension
      const mimeType = file.value.type as AllowedTypes
  
      if (!ALLOWED_TYPES[mimeType] && !['json', 'csv'].includes(extension)) {
        throw new Error('Only JSON and CSV files are allowed')
      }
  
      return true
    } else {
      return false
    }
  })

  function readFile<R extends string>(): Promise<R> {
    return new Promise<R>((resolve, reject) => {
      const reader = new FileReader()

      reader.onload = (e) => {
        try {
          if (e.target) {
            resolve(e.target.result as R)
          } else {
            reject(new Error('Failed to resolve target'))
          }
        } catch (e) {
          console.error(e)
          reject(new Error('Failed to read file content'))
        }
      }

      reader.onerror = () => {
        reject(new Error('File reading failed'))
      }

      if (isDefined(file)) {
        reader.readAsText(file.value)
      }
    })
  }

  function json(content: string) {
    try {
      const data = JSON.parse(content)

      if (data === null) {
        // Error
      }

      return data
    } catch (e) {
      if (e instanceof SyntaxError) {
        // Error
        return
      }
      // Error
      console.log(e)
    }
  }

  function csv<C extends ProcessedCsv<unknown>>(content: string): C {
    try {
      if (!content || content.trim().length === 0) {
        throw new Error('CSV file is empty')
      }

      // Import PapaParse (add to your package.json: npm install papaparse)
      // For Nuxt, you might need to import it dynamically or use a plugin

      const parseResult = parse<C>(content, {
        header: true,              // First row contains headers
        skipEmptyLines: true,      // Skip empty lines
        trimHeaders: true,         // Trim whitespace from headers
        dynamicTyping: false,      // Keep all values as strings for safety
        transformHeader: (header) => {
          // Clean the headers
          return header.trim().replace(/[^\w\s-]/g, '').replace(/\s+/g, '_')
        },
        transform: (value) => {
          // Basic sanitization of cell values
          return typeof value === 'string' ? value.trim() : value
        },
        delimitersToGuess: [',', '\t', '|', ';'], // Try multiple delimiters
        newline: '',               // Auto-detect line endings
        quoteChar: '"',
        escapeChar: '"',
        fastMode: false,           // More thorough parsing
        preview: 0,                // Parse all rows
        worker: false              // Don't use web workers for simplicity
      })

      // Check for parsing errors
      if (parseResult.errors && parseResult.errors.length > 0) {
        const criticalErrors = parseResult.errors.filter(error =>
          error.type === 'Delimiter' || error.type === 'Quotes'
        )

        if (criticalErrors.length > 0) {
          throw new Error(`CSV parsing failed: ${criticalErrors[0].message}`)
        }

        // Log non-critical errors but continue
        console.warn('CSV parsing warnings:', parseResult.errors)
      }

      // Validate parsed data
      if (!parseResult.data || parseResult.data.length === 0) {
        throw new Error('No data found in CSV file')
      }

      // Get headers from the first row keys
      const headers = parseResult.meta?.fields || Object.keys(parseResult.data[0] || {})

      if (headers.length === 0) {
        throw new Error('No headers found in CSV file')
      }

      // Additional validation
      const validRows = parseResult.data.filter((row: SingleRow<typeof parseResult.data[0]>) => {
        // Remove completely empty rows
        // return Object.values(row).some(value => value !== null && value !== undefined && value !== '')
        return Object.values(row)
      })

      // if (validRows.length === 0) {
      //   throw new Error('No valid data rows found in CSV file')
      // }

      // Check for reasonable number of columns (prevent potential attacks)
      if (headers.length > 100) {
        throw new Error('CSV file has too many columns (maximum 100 allowed)')
      }

      // Check for reasonable number of rows (prevent memory exhaustion)
      // if (validRows.length > 10000) {
      //   throw new Error('CSV file has too many rows (maximum 10,000 allowed)')
      // }

      return {
        headers,
        data: validRows,
        meta: {
          totalRows: validRows.length,
          totalColumns: headers.length,
          delimiter: parseResult.meta?.delimiter || ',',
          linebreak: parseResult.meta?.linebreak || '\n',
          aborted: parseResult.meta?.aborted || false,
          truncated: parseResult.meta?.truncated || false
        }
      }
    } catch (e) {
      console.error(e)

      return {
        headers: [],
        data: [],
        meta: {
          totalRows: 0,
          totalColumns: 0,
          delimiter: '',
          linebreak: '',
          aborted: false,
          truncated: false
        }
      }

      // Handle PapaParse specific errors
      // if (e.name === 'TypeError' && e.message.includes('Papa')) {
      //   throw new Error('CSV parser not available. Please install papaparse package.')
      // }
      // throw new Error(`CSV parsing error: ${e.message}`)
    }
  }

  const isProcessing = ref<boolean>(false)
  const processedData = ref<Undefineable<unknown>>()
  const dataPreview = ref<string>()

  async function process(selectedFile?: Refeable<Undefineable<_File>>) {
    isProcessing.value = true
    file.value = unref(selectedFile)

    try {
      if (isDefined(file)) {
        const content = await readFile()
        const extension = file.value.name.toLowerCase().split('.').pop() as Undefineable<FileExtension>

        if (extension == 'json' || file.value.type === 'application/json') {
          processedData.value = json(content)
          dataPreview.value = JSON.stringify(Array.isArray(processedData.value) ? processedData.value.slice(0, 5) : processedData.value, null, 2)
        } else {
          processedData.value = csv(content)

          if (isDefined(processedData)) {
            dataPreview.value = JSON.stringify(processedData.value.data.slice(0, 5), null, 2)
          }
        }
      }
    } catch (e) {
      console.log(e)
    } finally {
      isProcessing.value = false
    }
  }

  function downloadProcessedFile() {
    if (!processedData.value) return

    const dataStr = JSON.stringify(processedData.value, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)

    // const link = document.createElement('a')
    // link.href = url
    // link.download = `processed-${file.value.name.replace(/\.[^/.]+$/, '')}.json`
    // link.click()

    URL.revokeObjectURL(url)
  }

  function formatFileSize(bytes: number) {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return {
    isValid,
    processedData,
    isProcessing,
    formatFileSize,
    downloadProcessedFile,
    /**
     * Function used to read a file
     */
    process
  }
}
