package org.jay.sample.util

interface Logger {
    fun i(tag: String, message: String)
    fun e(tag: String, message: String)
    fun d(tag: String, message: String)
    fun w(tag: String, message: String)
}