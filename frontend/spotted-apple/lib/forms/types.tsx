import { ChangeEvent } from 'react'

export type FormAction = (payload: FormData) => void;

export type InputField = {
    id: string;
    placeHolder?: string;
    initialValue?: string;
    fieldType?: string;
    onChange?: (e: ChangeEvent<HTMLInputElement>) => void;
};

export type InputFields = InputField[];

export type ButtonDisplay = {
    staticDisplay: string | undefined;
    pendingDisplay: string;
}

export type InputFieldsErrors = {
    errors: string[];
}

export type InputFieldErrorState = Record<string, boolean>;
