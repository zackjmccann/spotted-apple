// This file contains type definitions for Spotted Apple data,
// describing the shape of data, data types, and what each property should accept.
export type User = {
    id: number,
    name: string,
    email: string,
    password: string,
    created: Date
}