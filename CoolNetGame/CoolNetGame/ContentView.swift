//
//  ContentView.swift
//  CoolNetGame
//
//  Created by Eugenio Tampieri on 22/06/21.
//

import SwiftUI

struct SetupView: View {
    @State private var name: String = ""
    @State private var address: String = ""
    @State private var port: String = "53000"
    var body: some View {
        VStack(){
        Text("CoolNetGame")
            .font(/*@START_MENU_TOKEN@*/.largeTitle/*@END_MENU_TOKEN@*/)
            .fontWeight(/*@START_MENU_TOKEN@*/.bold/*@END_MENU_TOKEN@*/)
            .foregroundColor(.green)
            .padding([.leading, .bottom, .trailing])
            HStack() {
                Label("Your name", systemImage:"person.fill")
                TextField("Your name", text: $name)
            }.padding([.leading, .trailing, .top])
            HStack() {
                Label("Server address", systemImage:"network")
                TextField("1.2.3.4", text: $address)
            }.padding([.leading, .trailing])
            HStack() {
                Label("Server port", systemImage:"network")
                TextField("53000", text: $port)
            }.padding([.leading, .trailing])
            Button("Connect", action: connect)
                .padding()
                .cornerRadius(10.0)
                .border(Color.green, width: /*@START_MENU_TOKEN@*/1/*@END_MENU_TOKEN@*/)
                .foregroundColor(.green)
                .font(/*@START_MENU_TOKEN@*/.title3/*@END_MENU_TOKEN@*/)
                .padding()
        }
    }
    private func connect() {
        var socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    }
}

struct SetupView_Previews: PreviewProvider {
    static var previews: some View {
        SetupView()
    }
}
