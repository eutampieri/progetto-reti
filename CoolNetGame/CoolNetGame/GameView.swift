//
//  GameView.swift
//  CoolNetGame
//
//  Created by Eugenio Tampieri on 22/06/21.
//

import SwiftUI

struct Choice {
    var label: String
    var id: String
}

struct GameView: View {
    @State private var question: String = ""
    private var options: [Choice] = []
    var body: some View {
        VStack {
            Text(question)

        }
    }
}

struct GameView_Previews: PreviewProvider {
    static var previews: some View {
        GameView()
    }
}
