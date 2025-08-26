package com.image_server2

import java.io.File
import java.io.FileInputStream
import java.net.Socket
import java.nio.ByteBuffer

object NetworkClient {

    fun sendImage(file: File, host: String, port: Int) {
        val socket = Socket(host, port)
        val output = socket.getOutputStream()

        val bytes = file.readBytes()

        // Envia tamanho da imagem (4 bytes)
        val sizeBuffer = ByteBuffer.allocate(4).putInt(bytes.size).array()
        output.write(sizeBuffer)

        // Envia imagem
        output.write(bytes)
        output.flush()

        socket.close()
    }
}
