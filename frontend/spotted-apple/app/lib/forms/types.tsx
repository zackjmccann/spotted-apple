import { ChangeEvent } from 'react'

export type InputField = {
    id: string;
    placeHolder?: string;
    initialValue?: string;
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
